from machine import ADC, Pin    
    
def read():    
    p2 = Pin(34)
    adc = ADC(p2)
    adc.atten(ADC.ATTN_11DB)
    return adc.read()