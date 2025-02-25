#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %%
def query_measurement(address):
    """
    ========== DESCRIPTION ==========

    This function can query the measurement value

    ========== FROM ==========

    Manual of Fluke 8842A

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
     
    ========== OUTPUT ==========
    
    <measurement>
        -- float --
        The measurement
        [depend]

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    answer = instru.query('F1')

    voltage = float(answer)

    ################## FUNCTION ###############################################

    return voltage
