   
from marshmallow import Schema, fields,post_load
from datetime import datetime

class SignalType():
    unDef = 'undef'
    temperature = 'temperature'
    class temperature_():
        outside = 'temperature_outside'
        flow = 'temperature_flow'
        returnFlow = 'temperature_return_flow'
        storage = 'temperature_storage'
        freezProtection = 'temperature_freez_protection'
        outsideTemperature = 'temperature_outside'    
        room = 'temperature_room'
        chiller = 'temperature_chiller'
        chillerFlow = 'temperature_chiller_flow'
        chillerReturnFlow = 'temperature_chiller_return_flow'
        chillerStorage = 'temperature_chiller_storage'
        
        
    setTemperature = 'set_temperature'
    class setTemperature_():
        heater = 'set_temperature_heater'
        class heater_():
            comfort = 'set_temperature_heater_comfort'
            setback = 'set_temperature_heater_setback'
        cooler = 'set_temperature_cooler'
        flow = 'set_temperature_flow'
        returnFlow = 'set_temperature_return_flow'
        storage = 'set_temperature_storage'
        room = 'set_temperature_room'
        conditioning = 'set_temperature_conditioning'
    humidity = 'humidity'
    windowIsOpen = 'window_is_open'
    presence = 'presence'
    motion = 'motion'
    presence_merged = 'presence_merged'
    illumination = 'illumination'
    co2 = 'co2'
    pressure = 'pressure'
    tvoc = 'tvoc'
    o3 = 'o3'
    pm10 = 'pm10'
    pm2_5 = 'pm2_5'
    open = 'open'
    close = 'close'
    actuatorValue = 'actuator_value'
    systemState = 'system_state'
    vdd = 'vdd'
    battery = 'battery'
    class systemState_():
        heater = 'system_state_heater'
        heaterMode = 'system_state_heater_mode'
        tapWater = 'system_state_tap_water'
        tapWaterMode = 'system_state_tap_water_mode'
        cooler = 'system_state_cooler'
        ventilation = 'system_state_ventilation'
        conditioning = 'system_state_conditioning'
    consumtion = 'consumption'
    class consumtion_():
        gas = 'consumption_gas'
        gasRel = 'consumption_gas_rel'
        gasCurrent = 'consumption_gas_current'
        power = 'consumption_power'
        powerRel = 'consumption_power_rel'
        powerCurrent = 'consumption_power_current'
        water = 'consumption_water'
        waterRel = 'consumption_water_rel'
        waterCurrent = 'consumption_water_current'
        heat = 'consumption_heat'
        heatRel = 'consumption_heat_rel'
        heatCurrent = 'consumption_heat_current'
        cool = 'consumption_cool'
        coolRel = 'consumption_cool_rel'
        coolCurrent = 'consumption_cool_current'    

    class curve_():
        outsideTemperature = 'curve_outside_temperature'
        flowTemperature = 'curve_flow_temperature'
        flowTemperatureEco = 'curve_flow_temperature_eco'
        returnFlowTemperature = 'curve_return_flow_temperature'
   
    
    valve = 'valve'
    class valve_():
        flow = 'valve_flow'
        returnFlow = 'valve_return_flow'
        heating = 'valve_heating'
        cooling = 'valve_cooling'
        tap = 'valve_tap'
        ventilation  = 'valve_ventilation'
        conditionoing = 'valve_conditioning'
    pump = 'pump'
    class pump_():
        heating = 'pump_heating'
        cooling = 'pump_cooling'
        tap = 'pump_tap'
        ventilation = 'pump_ventilation'
        conditionoing = 'pump_conditioning'
        input = 'pump_in'
        output = 'pump_out'
        circulation = 'pump_circulation'
    fan = 'fan'
    class fan_():
        ventilation = 'fan_ventilation'
        conditioning = 'fan_conditioning'
        
        
    
    ####### Deprecated ########
    # Aus Kompaitibitäsgründen bleiben alte definiton erstmal erhalteb
    consumptionGas = 'consumption_gas'
    consumptionGasRel = 'consumption_gas_rel'
    consumptionGasCurrent = 'consumption_gas_current'
    consumptionPower = 'consumption_power'
    consumptionPowerRel = 'consumption_power_rel'
    consumptionPowerCurrent = 'consumption_power_current'
    consumptionWater = 'consumption_water'
    consumptionWaterRel = 'consumption_water_rel'
    consumptionWaterCurrent = 'consumption_water_current'
    consumptionHeat = 'consumption_heat'
    consumptionHeatRel = 'consumption_heat_rel'
    consumptionHeatCurrent = 'consumption_heat_current'
    consumptionCool = 'consumption_cool'
    consumptionCoolRel = 'consumption_cool_rel'
    consumptionCoolCurrent = 'consumption_cool_current'
    
    
    flowTemperature = 'flow_temperature'
    returnFlowTemperature = 'return_flow_temperature'
    storageTemperature = 'storage_temperature'
    freezProtectionTemperature = 'freez_protection_temperature'
    outsideTemperature = 'outside_temperature'

class SignalOptionType():
    unDef = 'undef'
    forwardingMQTT = 'forwarding_mqtt'
    convertFrom    = 'convert_from'
    class buildingHardware():
        unDef = 'undef'
        heating = 'building_hardware_heating'
        heating_sub_system = 'building_hardware_heating_sub_system'
        cooling = 'building_hardware_cooling'
        ventilation = 'building_hardware_ventilation'
        lighting = 'building_hardware_lighting'
        energy = 'building_hardware_energy'
    
class SignalDirection():
    input = 'input'
    output = 'output'

def singnalDirection2Flags(direction):
    isInput = False
    isOutput = False
    if direction == SignalDirection.input:
        isInput = True
    elif direction == SignalDirection.output:
        isOutput = True
    return isInput,isOutput
    
class Signal():
    def __init__(self,type,component=0,group=0,ioDevice="",ioSignal="",parameter={},timestamp=datetime.now(),value = 0.0,valueStr = "",ext={}):
        self.timestamp  = timestamp
        self.component  = int(component)
        self.group      = int(group)
        self.ioDevice   = ioDevice
        self.ioSignal   = ioSignal
        self.type       = type
        self.value      = float(value)
        self.valueStr   = str(valueStr)
        self.ext        = dict(ext)
        
    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)
    def __str__(self) -> str:
        return f'component={self.component}, group={self.group}, ioDevice={self.ioDevice}, ioSignal={self.ioSignal}, type={self.type}, value={self.value}, valueStr={self.valueStr}, timestmap={self.timestamp}, ext={self.ext}'        

class SignalSchmea(Schema):
    timestamp   = fields.DateTime(required=True)
    component   = fields.Int()
    group       = fields.Int()
    ioDevice    = fields.Str()
    ioSignal    = fields.Str()
    type        = fields.Str()
    value       = fields.Float()
    valueStr    = fields.Str()
    ext         = fields.Dict()
    
    @post_load
    def make_control(self, data, **kwargs):
        return Signal(**data)