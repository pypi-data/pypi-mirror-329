#!/usr/bin/env python3

# %%
def query_identification(address):
    """
    ========== DESCRIPTION ==========

    This function can return the identification of the Cryocon Model 54

    ========== FROM ==========

    Manual of Cryo-con Model 54

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument (e.g. 'GPIB0::15::INSTR')

    ========== OUTPUT ==========

    <manufacturer>
        -- string --
        Should be "Cryo-con"

    <model>
        -- string --
        Should be "Model 54"

    <serial>
        -- string --
        Depend on your instrument

    <firmware_version>
        -- string --
        Depend on your instrument

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========

    from cryopy import instrument.cryocon.model54

    manufacturer,model,serial,firmware_version = model54.query_identification('GPIB0::15::INSTR')

    """

    ################## MODULES ###############################################

    import pyvisa

    ################## INITIALISATION ########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    answer = instru.query('*IDN?')

    manufacturer = answer[0:8]
    model = answer[9:17]
    serial = answer[18:24]
    firmware_version = answer[25:30]

    return manufacturer, model, serial, firmware_version


# %%
def query_input(address, channel):
    """
    ========== DESCRIPTION ==========

    This function can return the input of a given channel of the Cryocon Model 54

    ========== FROM ==========

    Manual of Cryo-con Model 54

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument (e.g. 'GPIB0::15::INSTR')

    <channel>
        -- string --
        The channel ('a','b','c' or 'd')

    ========== OUTPUT ==========

    <input>
        -- float --
        The input measured by the channel
        [K] or [Ohm]

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========

    from cryopy import instrument.cryocon.model54

    input = model54.query_input'GPIB0::15::INSTR','a')

    """

    ################## MODULES ###############################################

    import pyvisa
    import numpy

    ################## INITIALISATION ########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    answer = instru.query('input? ' + channel)

    try:
        value = float(answer)
        return value

    except ValueError:
        return numpy.nan


# %%
def control_sensor_unit(address, channel, unit):
    """
    ========== DESCRIPTION ==========

    This function can control the unit of a given channel of the Cryocon Model 54

    ========== FROM ==========

    Manual of Cryo-con Model 54

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument (e.g. 'GPIB0::15::INSTR')

    <channel>
        -- string --
        The channel ('a','b','c' or 'd')
        
    <unit>
        -- string --
        The unit ('k' for Kelvin , 's' for sensor)

    ========== OUTPUT ==========

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========

    from cryopy import instrument.cryocon.model54

    model54.control_sensor_unit('GPIB0::15::INSTR','a','k')

    """

    ################## MODULES ###############################################

    import pyvisa

    ################## INITIALISATION ########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    instru.write('input ' + channel + ':unit '+unit)
    
