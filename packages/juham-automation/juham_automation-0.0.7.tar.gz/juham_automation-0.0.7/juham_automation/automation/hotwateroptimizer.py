import json
from typing import Any
from typing_extensions import override

from masterpiece.mqtt import MqttMsg
from juham_core import Juham
from juham_core.timeutils import (
    quantize,
    timestamp,
    timestamp_hour,
    timestampstr,
    is_hour_within_schedule,
    timestamp_hour_local,
)


class HotWaterOptimizer(Juham):
    """Automation class for optimized control of temperature driven home energy consumers e.g hot
    water radiators. Reads spot prices, electricity forecast and temperatures to minimize electricity bill.
    Additional control over heating is provided by the following attributes

    Attributes:
        schedule_start_hour (float):  hour heating can start, in local time
        schedule_stop_hour (float):  hour heating is forced to stop
        start_hour (float): start_hour (int): ordinal of the first allowed electricity price slot to be consumed
        num_hours (int): the number of hour slots allowed

    Computes UOI - optimization utilization index for each hour, based on the spot price and the solar power forecast.
    Value of 0 means the hour is expensive, value of 1 means the hour is free. The UOI threshold determines the slots
    that are allowed to be consumed.


    """

    maximum_boiler_temperature = 70
    minimum_boiler_temperature = 40
    energy_balancing_interval: float = 3600
    radiator_power = 3000  # 3 kW
    operation_threshold = 5 * 60
    heating_hours_per_day = 4  # use the four cheapest hours per day
    schedule_start_hour: float = 0
    schedule_stop_hour: float = 0
    timezone = "Europe/Helsinki"
    expected_average_price = 0.2  # 20 eur per kWh
    uoi_threshold = 0.8

    def __init__(
        self,
        name: str,
        temperature_sensor: str,
        start_hour: int,
        num_hours: int,
        spot_limit: float,
    ) -> None:
        """Create power plan for automating temperature driven systems, e.g. heating radiators
        to optimize energy consumption based on electricity prices.

        Electricity Price MQTT Topic: This specifies the MQTT topic through which the controller receives
        hourly electricity price forecasts for the next day or two.
        Radiator Control Topic: The MQTT topic used to control the radiator relay.
        Temperature Sensor Topic: The MQTT topic where the temperature sensor publishes its readings.
        Electricity Price Slot Range: A pair of integers determining which electricity price slots the
        controller uses. The slots are ranked from the cheapest to the most expensive. For example:
        - A range of 0, 3 directs the controller to use electricity during the three cheapest hours.
        - A second controller with a range of 3, 2 would target the next two cheapest hours, and so on.
        Maximum Electricity Price Threshold: An upper limit for the electricity price, serving as an additional control.
        The controller only operates within its designated price slots if the prices are below this threshold.

        The maximum price threshold reflects the criticality of the radiator's operation:

        High thresholds indicate that the radiator should remain operational regardless of the price.
        Low thresholds imply the radiator can be turned off during expensive periods, suggesting it has a less critical role.

        By combining these attributes, the controller ensures efficient energy usage while maintaining desired heating levels.

        Args:
            name (str): name of the heating radiator
            temperature_sensor (str): temperature sensor of the heating radiator
            start_hour (int): ordinal of the first allowed electricity price slot to be consumed
            num_hours (int): the number of slots allowed
            spot_limit (float): maximum price allowed
        """
        super().__init__(name)

        self.heating_hours_per_day = num_hours
        self.start_hour = start_hour
        self.spot_limit = spot_limit

        self.topic_spot = self.make_topic_name("spot")
        self.topic_forecast = self.make_topic_name("forecast")
        self.topic_temperature = self.make_topic_name(temperature_sensor)
        self.topic_powerplan = self.make_topic_name("powerplan")
        self.topic_power = self.make_topic_name("power")
        self.topic_in_powerconsumption = self.make_topic_name("powerconsumption")
        self.topic_in_net_energy_balance = self.make_topic_name("net_energy_balance")

        self.current_temperature = 100
        self.current_heating_plan = 0
        self.current_relay_state = -1
        self.heating_plan: list[dict[str, int]] = []
        self.power_plan: list[dict[str, Any]] = []
        self.ranked_spot_prices: list[dict[Any, Any]] = []
        self.ranked_solarpower: list[dict[Any, Any]] = []
        self.relay: bool = False
        self.relay_started_ts: float = 0
        self.current_power: float = 0
        self.net_energy_balance: float = 0.0
        self.net_energy_power: float = 0
        self.net_energy_balance_ts: float = 0
        self.net_energy_balancing_rc: bool = False
        self.net_energy_balancing_mode = False

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_spot)
            self.subscribe(self.topic_forecast)
            self.subscribe(self.topic_temperature)
            self.subscribe(self.topic_in_powerconsumption)
            self.subscribe(self.topic_in_net_energy_balance)

    def sort_by_rank(
        self, hours: list[dict[str, Any]], ts_utc_now: float
    ) -> list[dict[str, Any]]:
        """Sort the given electricity prices by their rank value. Given a list
        of electricity prices, return a sorted list from the cheapest to the
        most expensive hours. Entries that represent electricity prices in the
        past are excluded.

        Args:
            hours (list): list of hourly electricity prices
            ts_utc_now (float): current time

        Returns:
            list: sorted list of electricity prices
        """
        sh = sorted(hours, key=lambda x: x["Rank"])
        ranked_hours = []
        for h in sh:
            utc_ts = h["Timestamp"]
            if utc_ts > ts_utc_now:
                ranked_hours.append(h)

        return ranked_hours

    def sort_by_power(
        self, solarpower: list[dict[Any, Any]], ts_utc: float
    ) -> list[dict[Any, Any]]:
        """Sort forecast of solarpower to decreasing order.

        Args:
            solarpower (list): list of entries describing hourly solar energy forecast
            ts_utc(float): start time, for exluding entries that are in the past

        Returns:
            list: list from the highest solarenergy to lowest.
        """

        # if all items have solarenergy key then
        # sh = sorted(solarpower, key=lambda x: x["solarenergy"], reverse=True)
        # else skip items that don't have solarenergy key
        sh = sorted(
            [item for item in solarpower if "solarenergy" in item],
            key=lambda x: x["solarenergy"],
            reverse=True,
        )
        self.debug(
            f"Sorted {len(sh)} days of forecast starting at {timestampstr(ts_utc)}"
        )
        ranked_hours = []

        for h in sh:
            utc_ts: float = float(h["ts"])
            if utc_ts >= ts_utc:
                ranked_hours.append(h)
        self.debug(f"Forecast sorted for the next {str(len(ranked_hours))} hours")
        return ranked_hours

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        m = None
        ts: float = timestamp()
        ts_utc_quantized: float = quantize(3600, ts - 3600)
        if msg.topic == self.topic_spot:
            self.ranked_spot_prices = self.sort_by_rank(
                json.loads(msg.payload.decode()), ts_utc_quantized
            )
            self.debug(
                f"Spot prices received and ranked for {len(self.ranked_spot_prices)} hours"
            )
            self.power_plan = []  # reset power plan, it depends on spot prices
            return
        elif msg.topic == self.topic_forecast:
            forecast = json.loads(msg.payload.decode())
            # reject messages that don't have  solarenergy forecast

            for f in forecast:
                if not "solarenergy" in f:
                    return

            self.ranked_solarpower = self.sort_by_power(forecast, ts_utc_quantized)
            self.debug(
                f"Solar energy forecast received and ranked for {len(self.ranked_solarpower)} hours"
            )
            self.power_plan = []  # reset power plan, it depends on forecast
            return
        elif msg.topic == self.topic_temperature:
            m = json.loads(msg.payload.decode())
            self.current_temperature = m["temperature"]
        elif msg.topic == self.topic_in_net_energy_balance:
            m = json.loads(msg.payload.decode())
            self.net_energy_balance = m["energy"]
            self.net_energy_power = m["power"]
        elif msg.topic == self.topic_in_powerconsumption:
            m = json.loads(msg.payload.decode())
            self.current_power = m["real_total"]
        else:
            super().on_message(client, userdata, msg)
            return
        self.on_powerplan(ts)

    def on_powerplan(self, ts_utc_now: float) -> None:
        """Apply power plan.

        Args:
            ts_utc_now (float): utc time
        """

        # optimization, check only once a minute
        elapsed: float = ts_utc_now - self.relay_started_ts
        if elapsed < 60:
            return
        self.relay_started_ts = ts_utc_now

        if not self.ranked_spot_prices:
            self.debug("Waiting  spot prices...", "")
            return

        if not self.power_plan:
            self.power_plan = self.create_power_plan()
            self.heating_plan = []
            self.info(
                f"Power plan of length {len(self.power_plan)} created",
                str(self.power_plan),
            )

        if not self.power_plan:
            self.error("Failed to create a power plan", "")
            return

        if len(self.power_plan) < 3:
            self.warning(
                f"Suspiciously short {len(self.power_plan)}  power plan, wait more data ..",
                "",
            )
            self.heating_plan = []
            self.power_plan = []
            return

        if not self.ranked_solarpower or len(self.ranked_solarpower) < 4:
            self.warning(
                f"Short of forecast {len(self.ranked_solarpower)}, optimization compromised..",
                "",
            )

        if not self.heating_plan:
            self.heating_plan = self.create_heating_plan()
            if not self.heating_plan:
                self.error("Failed to create heating plan")
                return
            else:
                self.info(
                    f"Heating plan of length {len(self.heating_plan)} created", ""
                )
        if len(self.heating_plan) < 3:
            self.info(f"Short heating plan {len(self.heating_plan)}, no can do", "")
            self.heating_plan = []
            self.power_plan = []
            return

        relay = self.consider_heating(ts_utc_now)
        if self.current_relay_state != relay:
            heat = {"Unit": self.name, "Timestamp": ts_utc_now, "State": relay}
            self.publish(self.topic_power, json.dumps(heat), 1, False)
            self.info(
                f"Relay state {self.name} changed to {relay} at {timestampstr(ts_utc_now)}",
                "",
            )
            self.current_relay_state = relay

    def consider_net_energy_balance(self, ts: float) -> bool:
        """Check when there is enough energy available for the radiators heat
        the water the remaining time within the  balancing interval,
        and switch the balancing mode on. If the remaining time in the
        current balancing slot is less than the threshold then
        optimize out.


        Args:
            ts (float): current time

        Returns:
            bool: true if production exceeds the consumption
        """

        # elapsed and remaining time within the current balancing slot
        elapsed_ts = ts - quantize(self.energy_balancing_interval, ts)
        remaining_ts = self.energy_balancing_interval - elapsed_ts

        # don't bother to switch the relay on for small intervals, to avoid
        # wearing contactors out
        if remaining_ts < self.operation_threshold:
            return False

        # check if the balance is sufficient for heating the next half of the energy balancing interval
        # if yes then switch heating on for the next half an hour
        needed_energy = 0.5 * self.radiator_power * remaining_ts
        elapsed_interval = ts - self.net_energy_balance_ts
        if (
            self.net_energy_balance > needed_energy
        ) and not self.net_energy_balancing_rc:
            self.net_energy_balance_ts = ts
            self.net_energy_balancing_rc = True  # heat
            # self.info("Enough to supply the radiator, enable")
            self.net_energy_balancing_mode = True  # balancing mode indicator on
        else:
            # check if we have reach the end of the interval, or consumed all the energy
            # of the current slot. If so switch the energy balancer mode off
            if (
                elapsed_interval > self.energy_balancing_interval / 2.0
                or self.net_energy_balance < 0
            ):
                self.net_energy_balancing_rc = False  # heating off
                # self.info("Balance used, or the end of the interval reached, disable")
        return self.net_energy_balancing_rc

    def consider_heating(self, ts: float) -> int:
        """Consider whether the target boiler needs heating.

        Args:
            ts (float): current UTC time

        Returns:
            int: 1 if heating is needed, 0 if not
        """

        # check if we have energy to consume, if so return 1
        if self.consider_net_energy_balance(ts):
            self.warning("TODO: Net energy balance positive, but disabled for now")
            # return 1
        elif self.net_energy_balancing_mode:
            balancing_slot_start_ts = quantize(self.energy_balancing_interval, ts)
            elapsed_b = ts - balancing_slot_start_ts
            if elapsed_b > self.energy_balancing_interval:
                self.net_energy_balancing_mode = False
                self.info(
                    f"TODO: Net energy balancing mode because elapsed {elapsed_b}s is less than balancing interval {self.energy_balancing_interval}s"
                )
            else:
                self.info(
                    f"TODO: Net energy balance waiting interval {elapsed_b}s to end"
                )
                # return 0

        if self.current_temperature > self.maximum_boiler_temperature:
            self.info(
                f"Current temperature {self.current_temperature}C already beyond max {self.maximum_boiler_temperature}C"
            )
            return 0
        hour = timestamp_hour(ts)

        for pp in self.heating_plan:
            ppts: float = pp["Timestamp"]
            h: float = timestamp_hour(ppts)
            if h == hour:
                return pp["State"]

        self.error(f"Cannot find heating plan for hour {hour}")
        return 0

    # compute figure of merit (FOM) for each hour
    # the higher the solarenergy and the lower the spot the higher the FOM

    # compute utilization optimization index
    def compute_uoi(
        self,
        price: float,
        hour: float,
    ) -> float:
        """Compute UOI - utilization optimization index.

        Args:
            price (float): effective price for this device
            hour  (float) : the hour of the day

        Returns:
            float: utilization optimization index
        """

        if not is_hour_within_schedule(
            hour, self.schedule_start_hour, self.schedule_stop_hour
        ):
            return 0.0

        if price < 0.0001:
            return 1.0  # use
        elif price > self.expected_average_price:
            return 0.0  # try not to use
        else:
            fom = self.expected_average_price / price
            return fom

    def compute_effective_price(
        self, requested_power: float, available_solpower: float, spot: float
    ) -> float:
        """Compute effective electricity price. If there is enough solar power then
        electricity price is zero.

        Args:
            requested_power (float): requested power
            available_solpower (float): current solar power forecast
            spot (float): spot price
            hour  (float) : the hour of the day

        Returns:
            float: effective price for the requested power
        """

        # if we have enough solar power, use it
        if requested_power < available_solpower:
            return 0.0

        # check how  much of the power is solar and how much is from the grid
        solar_factor: float = available_solpower / requested_power

        effective_spot: float = spot * (1 - solar_factor)

        return effective_spot

    def create_power_plan(self) -> list[dict[Any, Any]]:
        """Create power plan.

        Returns:
            list: list of utilization entries
        """
        ts_utc_quantized = quantize(3600, timestamp() - 3600)
        starts: str = timestampstr(ts_utc_quantized)
        self.info(
            f"Trying to create power plan starting at {starts} with {len(self.ranked_spot_prices)}  hourly spot prices",
            "",
        )

        # syncronize spot and solarenergy by timestamp
        spots = []
        for s in self.ranked_spot_prices:
            if s["Timestamp"] > ts_utc_quantized:
                spots.append(
                    {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
                )

        if len(spots) == 0:
            self.debug(
                f"No spot prices initialized yet, can't proceed",
                "",
            )
        self.info(
            f"Have spot prices for the next {len(spots)} hours",
            "",
        )
        powers = []
        for s in self.ranked_solarpower:
            if s["ts"] >= ts_utc_quantized:
                powers.append({"Timestamp": s["ts"], "Solarenergy": s["solarenergy"]})

        num_powers: int = len(powers)
        if num_powers == 0:
            self.debug(
                f"No solar forecast initialized yet, proceed without solar forecast",
                "",
            )
        else:
            self.debug(
                f"Have solar forecast  for the next {num_powers} hours",
                "",
            )
        hplan = []
        hour: float = 0
        if len(powers) >= 8:  # at least 8 hours of solar energy forecast
            for spot, solar in zip(spots, powers):
                ts = spot["Timestamp"]
                solarenergy = solar["Solarenergy"]
                spotprice = spot["PriceWithTax"]
                effective_price: float = self.compute_effective_price(
                    self.radiator_power, solarenergy, spotprice
                )
                hour = timestamp_hour_local(ts, self.timezone)
                fom = self.compute_uoi(spotprice, hour)
                plan = {
                    "Timestamp": ts,
                    "FOM": fom,
                    "Spot": effective_price,
                }
                hplan.append(plan)
        else:  # no solar forecast available, assume no free energy available
            for spot in spots:
                ts = spot["Timestamp"]
                solarenergy = 0.0
                spotprice = spot["PriceWithTax"]
                effective_price = spotprice  # no free energy available
                hour = timestamp_hour_local(ts, self.timezone)
                fom = self.compute_uoi(effective_price, hour)
                plan = {
                    "Timestamp": spot["Timestamp"],
                    "FOM": fom,
                    "Spot": effective_price,
                }
                hplan.append(plan)

        shplan = sorted(hplan, key=lambda x: x["FOM"], reverse=True)

        self.debug(f"Powerplan starts {starts} up to {len(shplan)} hours")
        return shplan

    def enable_relay(
        self, hour: float, spot: float, fom: float, end_hour: float
    ) -> bool:
        return (
            hour >= self.start_hour
            and hour < end_hour
            and float(spot) < self.spot_limit
            and fom > self.uoi_threshold
        )

    def create_heating_plan(self) -> list[dict[str, Any]]:
        """Create heating plan.

        Returns:
            int: list of heating entries
        """

        state = 0
        heating_plan = []
        hour: int = 0
        for hp in self.power_plan:
            ts: float = hp["Timestamp"]
            fom = hp["FOM"]
            spot = hp["Spot"]
            end_hour: float = self.start_hour + self.heating_hours_per_day
            local_hour: float = timestamp_hour_local(ts, self.timezone)
            schedule_on: bool = is_hour_within_schedule(
                local_hour, self.schedule_start_hour, self.schedule_stop_hour
            )

            if self.enable_relay(hour, spot, fom, end_hour) and schedule_on:
                state = 1
            else:
                state = 0
            heat = {
                "Unit": self.name,
                "Timestamp": ts,
                "State": state,
                "Schedule": schedule_on,
                "UOI": fom,
                "Spot": spot,
            }

            self.publish(self.topic_powerplan, json.dumps(heat), 1, False)
            heating_plan.append(heat)
            hour = hour + 1

        self.info(f"Heating plan of {len(heating_plan)} hours created", "")
        return heating_plan
