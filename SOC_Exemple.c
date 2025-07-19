// SOC_Exemple.c

void initial_soc (int32_t* init_soc, int32_t min_voltage) {
    // 3rd degree Voltage to Capacity Mapping equation
    float init_soc_uc = -0.0955f * min_voltage * min_voltage * min_voltage + 43.5139f * min_voltage * min_voltage - 227.6142f * min_voltage + 300.7951f;
    
    // Value clamping
    if (init_soc_uc < 0) {
        *init_soc = 0;
    } else if (init_soc_uc > 100) {
        *init_soc = 100;
    } else {
        *init_soc = (int32_t)init_soc_uc;
    }
    
    if (min_voltage == 0) { // If the BMS is not connected or no message is received
        *init_soc = 0;
    }
}

void handle_soc (
    int32_t* soc, int32_t init_soc, float avg_current, float tick, float* discharge_sum, int32_t Capacity
) {
    float bp_current = -avg_current; // Invert current for discharge calculation
    if (bp_current == 0) { // If the BMS is not connected or no message is received
        bp_current = 0;
    }
    
    float current_period = 1.0f / tick; // Convert tick to seconds
    float discharge = (bp_current * current_period) / 3600.0f; // Convert to Ah
    *discharge_sum += discharge; // Update discharge sum in Ah

    float soc_uc = init_soc - (*discharge_sum / (float)Capacity) * 100.0f; // Coloumb counting SOC calculation

    // Value clamping
    if (soc_uc < 0) {
        *soc = 0;
    } else if (soc_uc > 100) {
        *soc = 100;
    } else {
        *soc = (int32_t)soc_uc;
    }
}