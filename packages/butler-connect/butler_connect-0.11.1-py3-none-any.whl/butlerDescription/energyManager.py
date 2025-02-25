from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


class SignalCollectionType():
    keyIndicator = 'key_indicator'
    consumption = 'consumption'
    measurement = 'measurement'
    
    _label_map = {
        keyIndicator: "Kennzahlen",
        consumption: "Verbrauchswerte",
        measurement: "Messwerte",
    }
    
    @classmethod
    def get_label(cls, collection_type):
        """Gibt das lesbare Label für einen gegebenen Signaltyp zurück."""
        return cls._label_map.get(collection_type, "Unbekannt")
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
    
class SignalType():
    unDef = 'undef'
    currentValue = 'current_value'
    meterReading = 'meter_reading'
    meterReadingRef = 'meter_reading_reference'
    consumption = 'consumption'
    consumptionRef = 'consumption_reference'
    currentConsumption = 'current_consumption'  # Aktueller Verbrauch (z. B. letzte Stunde)
    averageConsumption = 'average_consumption'  # Durchschnittsverbrauch über eine bestimmte Zeitspanne
    peakConsumption = 'peak_consumption'  # Spitzenverbrauch in einer Periode
    minConsumption = 'min_consumption'  # Minimalverbrauch in einer Periode
    totalConsumption = 'total_consumption'  # Gesamter Verbrauch über eine Periode
    powerOutput = 'power_output'  # Aktuelle Leistung (z. B. von Solaranlage)
    energyProduction = 'energy_production'  # Gesamtenergieproduktion einer Quelle
    costEstimation = 'cost_estimation'  # Geschätzte Kosten für einen bestimmten Verbrauch
    co2Emissions = 'co2_emissions'  # CO2-Emissionen basierend auf Verbrauchsdaten
    
     # Mapping der Signaltypen zu lesbaren Labels
    _label_map = {
        unDef: "Unbestimmt",
        currentValue: "Aktueller Wert",
        meterReading: "Zählerstand",
        meterReadingRef: "Referenzzählerstand",
        consumption: "Verbrauch",
        consumptionRef: "Referenzverbrauch",
        currentConsumption: "Aktueller Verbrauch",
        averageConsumption: "Durchschnittsverbrauch",
        peakConsumption: "Spitzenverbrauch",
        minConsumption: "Minimalverbrauch",
        totalConsumption: "Gesamtverbrauch",
        powerOutput: "Leistung",
        energyProduction: "Energieproduktion",
        costEstimation: "Kostenabschätzung",
        co2Emissions: "CO2-Emissionen",
    }

    @classmethod
    def get_label(cls, signal_type):
        """Gibt das lesbare Label für einen gegebenen Signaltyp zurück."""
        return cls._label_map.get(signal_type, "Unbekannt")
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
    
class Unit():
    # Allgemein
    unDef = 'undef'

    # Energieeinheiten
    watt = 'W'  # Watt
    kilowatt = 'kW'  # Kilowatt
    megawatt = 'MW'  # Megawatt
    gigawatt = 'GW'  # Gigawatt
    wattHour = 'Wh'  # Wattstunde
    kilowattHour = 'kWh'  # Kilowattstunde
    megawattHour = 'MWh'  # Megawattstunde
    gigawattHour = 'GWh'  # Gigawattstunde
    joule = 'J'  # Joule
    kilojoule = 'kJ'  # Kilojoule
    megajoule = 'MJ'  # Megajoule

    # Leistung (Power)
    voltAmpere = 'VA'  # Voltampere (Scheinleistung)
    kilovoltAmpere = 'kVA'  # Kilovoltampere
    megavoltAmpere = 'MVA'  # Megavoltampere
    voltAmpereReactive = 'VAR'  # Blindleistung
    kilovoltAmpereReactive = 'kVAR'  # Kilovoltampere Blindleistung
    powerFactor = 'PF'  # Leistungsfaktor

    # Elektrische Spannung und Stromstärke
    volt = 'V'  # Volt
    millivolt = 'mV'  # Millivolt
    kilovolt = 'kV'  # Kilovolt
    ampere = 'A'  # Ampere
    milliampere = 'mA'  # Milliampere
    kiloampere = 'kA'  # Kiloampere
    ohm = 'Ω'  # Ohm (Widerstand)

    # Frequenz
    hertz = 'Hz'  # Hertz
    kilohertz = 'kHz'  # Kilohertz
    megahertz = 'MHz'  # Megahertz

    # Gas- und Wassereinheiten
    cubicMeter = 'm³'  # Kubikmeter
    liter = 'L'  # Liter
    milliliter = 'mL'  # Milliliter
    gallon = 'gal'  # Gallone

    # Druck
    pascal = 'Pa'  # Pascal
    kilopascal = 'kPa'  # Kilopascal
    bar = 'bar'  # Bar

    # Temperatur
    celsius = '°C'  # Grad Celsius
    fahrenheit = '°F'  # Grad Fahrenheit
    kelvin = 'K'  # Kelvin

    # CO2-Emissionen
    gramCO2 = 'gCO2'  # Gramm CO2
    kilogramCO2 = 'kgCO2'  # Kilogramm CO2
    tonCO2 = 'tCO2'  # Tonne CO2

    # Zeitangaben
    second = 's'  # Sekunde
    minute = 'min'  # Minute
    hour = 'h'  # Stunde
    day = 'd'  # Tag
    week = 'w'  # Woche
    month = 'M'  # Monat
    year = 'Y'  # Jahr

    # Mapping für lesbare Labels
    _label_map = {
        unDef: "Unbestimmt",
        watt: "Watt",
        kilowatt: "Kilowatt",
        megawatt: "Megawatt",
        gigawatt: "Gigawatt",
        wattHour: "Wattstunde",
        kilowattHour: "Kilowattstunde",
        megawattHour: "Megawattstunde",
        gigawattHour: "Gigawattstunde",
        joule: "Joule",
        kilojoule: "Kilojoule",
        megajoule: "Megajoule",
        voltAmpere: "Voltampere",
        kilovoltAmpere: "Kilovoltampere",
        megavoltAmpere: "Megavoltampere",
        voltAmpereReactive: "Voltampere Blindleistung",
        kilovoltAmpereReactive: "Kilovoltampere Blindleistung",
        powerFactor: "Leistungsfaktor",
        volt: "Volt",
        millivolt: "Millivolt",
        kilovolt: "Kilovolt",
        ampere: "Ampere",
        milliampere: "Milliampere",
        kiloampere: "Kiloampere",
        ohm: "Ohm",
        hertz: "Hertz",
        kilohertz: "Kilohertz",
        megahertz: "Megahertz",
        cubicMeter: "Kubikmeter",
        liter: "Liter",
        milliliter: "Milliliter",
        gallon: "Gallone",
        pascal: "Pascal",
        kilopascal: "Kilopascal",
        bar: "Bar",
        celsius: "Grad Celsius",
        fahrenheit: "Grad Fahrenheit",
        kelvin: "Kelvin",
        gramCO2: "Gramm CO2",
        kilogramCO2: "Kilogramm CO2",
        tonCO2: "Tonne CO2",

        second: "Sekunde",
        minute: "Minute",
        hour: "Stunde",
        day: "Tag",
        week: "Woche",
        month: "Monat",
        year: "Jahr",
    }

    @classmethod
    def get_label(cls, unit):
        """Gibt das lesbare Label für eine gegebene Einheit zurück."""
        return cls._label_map.get(unit, "Unbekannt")
    
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
