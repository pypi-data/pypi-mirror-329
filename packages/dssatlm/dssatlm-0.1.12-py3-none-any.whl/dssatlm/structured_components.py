
weather_query_json_structure = f"""
    {{
        "farm_name": "-99",
        "crop": "-99",
        "latitude": -99,
        "longitude": -99,
        "elevation": -99,
        "focus": "-99",
        "planting_date": "-99",
        "Crop establishment phase": {{
            "season_alias": "-99",
            "phase_number_or_sequence": [
                -99
            ],
            "starting_date": "-99",
            "ending_date": "-99",
            "number_days": -99,
            "precipitation": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_min": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_max": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_mean": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }}
        }},
        "Vegetative growth phase": {{
            "season_alias": "-99",
            "phase_number_or_sequence": [
                -99
            ],
            "starting_date": "-99",
            "ending_date": "-99",
            "number_days": -99,
            "precipitation": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_min": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_max": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_mean": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }}
        }},
        "Yield formation phase": {{
            "season_alias": "-99",
            "phase_number_or_sequence": [
                -99
            ],
            "starting_date": "-99",
            "ending_date": "-99",
            "number_days": -99,
            "precipitation": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_min": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_max": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_mean": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }}
        }},
        "Entire Period": {{
            "season_alias": "-99",
            "phase_number_or_sequence": [
                -99,
                -99,
                -99
            ],
            "starting_date": "-99",
            "ending_date": "-99",
            "number_days": -99,
            "precipitation": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_min": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_max": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }},
            "temperature_mean": {{
                "value": -99,
                "unit": "-99",
                "type": "-99"
            }}
        }}
    }} 
"""

soil_query_json_structure = f"""
{{
    "farm_name": "-99",
    "crop": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "focus": "-99",
    "planting_date": "-99",
    "soil_profile_name": "-99",
    "soil_data_source": "-99",
    "soil_texture": "-99",
    "soil_series_name": "-99",
    "soil_depth": -99,
    "soil_site_name": -99,
    "soil_country_name": "-99",
    "soil_classification_family": "-99",
    "soil_surface_profile": {{
        "soil_color": {{
            "value": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_albedo": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_evalopration_limit": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_drainage_coefficient": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_runoff_curve_no": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_mineralization_factor": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_photosynthesis_factor": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_ph_in_buffer_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_phosphorus_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_potassium_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }}
    }},
    "soil_subsurface_profile": {{
        "soil_depth_bottom_layers": {{
            "number_of_depths": -99,
            "layer_1": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_2": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_3": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_4": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_5": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_6": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }}
        }},
        "soil_master_horizon": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_lower_limit": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_upper_limit_drained": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_upper_limit_saturated": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_root_growth_factor": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_sat_hydraulic_conductivity": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_bulk_density_moist": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_organic_carbon": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_clay": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_silt": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_coarse_fraction": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_total_nitrogen": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_ph_in_water": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_ph_in_buffer": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_cation_exchange_capacity": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_sadc": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }}
    }}
}}
"""

soil_surface_query_json_structure = f"""
{{
    "farm_name": "-99",
    "crop": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "focus": "-99",
    "planting_date": "-99",
    "soil_profile_name": "-99",
    "soil_data_source": "-99",
    "soil_texture": "-99",
    "soil_series_name": "-99",
    "soil_depth": -99,
    "soil_site_name": -99,
    "soil_country_name": "-99",
    "soil_classification_family": "-99",
    "soil_surface_profile": {{
        "soil_color": {{
            "value": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_albedo": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_evalopration_limit": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_drainage_coefficient": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_runoff_curve_no": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_mineralization_factor": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_photosynthesis_factor": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_ph_in_buffer_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_phosphorus_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }},
        "soil_potassium_determination_code": {{
            "value": -99,
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99"
        }}
    }},
    "soil_subsurface_profile": -99,
}}
"""

soil_subsurface_query_json_structure = f"""
{{
    "farm_name": "-99",
    "crop": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "focus": "-99",
    "planting_date": "-99",
    "soil_profile_name": "-99",
    "soil_data_source": "-99",
    "soil_texture": "-99",
    "soil_series_name": "-99",
    "soil_depth": -99,
    "soil_site_name": -99,
    "soil_country_name": "-99",
    "soil_classification_family": "-99",
    "soil_surface_profile": -99,
    "soil_subsurface_profile": {{
        "soil_depth_bottom_layers": {{
            "number_of_depths": -99,
            "layer_1": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_2": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_3": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_4": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_5": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }},
            "layer_6": {{
                "depth_value": -99,
                "depth_unit": "-99"
            }}
        }},
        "soil_master_horizon": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_lower_limit": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_upper_limit_drained": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_upper_limit_saturated": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_root_growth_factor": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_sat_hydraulic_conductivity": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_bulk_density_moist": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_organic_carbon": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_clay": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_silt": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_coarse_fraction": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_total_nitrogen": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_ph_in_water": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_ph_in_buffer": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_cation_exchange_capacity": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }},
        "soil_sadc": {{
            "layer_1": "-99",
            "layer_2": "-99",
            "layer_3": "-99",
            "layer_4": "-99",
            "layer_5": "-99",
            "layer_6": "-99",
            "soil_code": "-99",
            "code_in_dssat": "-99",
            "desciption": "-99",
            "unit": "-99.0"
        }}
    }}
}}
"""

crop_query_json_structure = f"""
{{
    "farm_name": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "planting_date": "-99",
    "focus": "-99",
    "crop": "-99",
    "crop_variety_name": "-99",
    "crop_ecotype_details": {{
      "crop_model": "-99",
      "crop_name": "-99",
      "ECO#": "-99",
      "ECONAME": "-99",
      "MG": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "TM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "THVAR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PL-EM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "EM-V1": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "V1-JU": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "JU-R0": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PM06": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PM09": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "LNGSH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "R7-R8": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-VS": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "TRIFL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "RWDTH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "RHGHT": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "R1PPO": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "OPTBI": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SLOBI": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }}
    }},
    "crop_genotype_details": {{
      "crop_model": "-99",
      "crop_name": "-99",
      "VAR#": "-99",
      "VAR-NAME": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "EXPNO": "-99",
      "ECO#": "-99",
      "CSDL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PPSEN": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "EM-FL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-SH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-SD": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SD-PM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-LF": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "LFMAX": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SLAVR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SIZLF": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "XFRT": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "WTPSD": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SFDUR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDPDV": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PODUR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "THRSH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDPRO": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDLIP": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }}
    }},
  }}
"""

crop_genotype_query_json_structure = f"""
{{
    "farm_name": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "planting_date": "-99",
    "focus": "-99",
    "crop": "-99",
    "crop_variety_name": "-99",
    "crop_ecotype_details": -99,
    "crop_genotype_details": {{
      "crop_model": "-99",
      "crop_name": "-99",
      "VAR#": "-99",
      "VAR-NAME": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "EXPNO": "-99",
      "ECO#": "-99",
      "CSDL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PPSEN": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "EM-FL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-SH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-SD": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SD-PM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-LF": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "LFMAX": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SLAVR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SIZLF": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "XFRT": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "WTPSD": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SFDUR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDPDV": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PODUR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "THRSH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDPRO": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SDLIP": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }}
    }},
}}
"""

crop_ecotype_query_json_structure = f"""
{{
    "farm_name": "-99",
    "latitude": -99,
    "longitude": -99,
    "elevation": -99,
    "planting_date": "-99",
    "focus": "-99",
    "crop": "-99",
    "crop_variety_name": "-99",
    "crop_ecotype_details": {{
      "crop_model": "-99",
      "crop_name": "-99",
      "ECO#": "-99",
      "ECONAME": "-99",
      "MG": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "TM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": "-99",
        "is_a_coefficient": -99
      }},
      "THVAR": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PL-EM": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "EM-V1": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "V1-JU": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "JU-R0": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PM06": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "PM09": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "LNGSH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "R7-R8": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "FL-VS": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "TRIFL": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "RWDTH": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "RHGHT": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "R1PPO": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "OPTBI": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }},
      "SLOBI": {{
        "coefficient_code": "-99",
        "coefficient_definition": "-99",
        "coefficient_unit": "-99",
        "coefficient_category": "-99",
        "coefficient_value": -99,
        "is_a_coefficient": -99
      }}
    }},
    "crop_genotype_details": -99,
  }}
"""



FARM_COMPONENTS_TO_STRUCT_MAP = {
    "weather": weather_query_json_structure,
    "soil": soil_query_json_structure,
    "soil_surface": soil_surface_query_json_structure,
    "soil_subsurface": soil_subsurface_query_json_structure,
    "crop": crop_query_json_structure,
    "crop_genotype": crop_genotype_query_json_structure,
    "crop_ecotype": crop_ecotype_query_json_structure,
}
