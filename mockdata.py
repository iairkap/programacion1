
""" ["id", "patente", "tipo_slot", "ocupado", "reservado_mensual", "hora_entrada", "tipo_vehiculo_estacionado"] """


GARAGE = [
    # PLANTA BAJA (piso 0) - 3x4 slots
    [
        """ {
            "id": 1, 
            "patente": "", 
            "tipo_slot": 1, 
            "ocupado": False, 
            "reservado_mensual": False, 
            "hora_entrada": None,
            "tipo_vehiculo_estacionado": 0
            },    
        {"id": 2, "patente": "ABC123", "tipo_slot": 2, "ocupado": False, "reservado_mensual": False, "hora_entrada": "2025-09-04 08:30", "tipo_vehiculo_estacionado": 2},
        {"id": 3, "patente": "", "tipo_slot": 2, "ocupado": False, "reservado_mensual": True, "hora_entrada": None, "tipo_vehiculo_estacionado": 0},    
        {"id": 4, "patente": "DEF456", "tipo_slot": 3, "ocupado": True, "reservado_mensual": False, "hora_entrada": "2025-09-04 09:15", "tipo_vehiculo_estacionado": 3},
        {"id": 5, "patente": "GHI789", "tipo_slot": 1, "ocupado": True, "reservado_mensual": False, "hora_entrada": "2025-09-04 07:45", "tipo_vehiculo_estacionado": 1}, 
        {"id": 6, "patente": "", "tipo_slot": 4, "ocupado": False, "reservado_mensual": False, "hora_entrada": None, "tipo_vehiculo_estacionado": 0},
        {"id": 7, "patente": "", "tipo_slot": 2, "ocupado": False, "reservado_mensual": False, "hora_entrada": None, "tipo_vehiculo_estacionado": 0}, 
        {"id": 8, "patente": "JKL012", "tipo_slot": 2, "ocupado": True, "reservado_mensual": True, "hora_entrada": "2025-09-04 10:00", "tipo_vehiculo_estacionado": 2},
        {"id": 9, "patente": "", "tipo_slot": 1, "ocupado": False, "reservado_mensual": False, "hora_entrada": None, "tipo_vehiculo_estacionado": 0},   
        {"id": 10, "patente": "MNO345", "tipo_slot": 4, "ocupado": True, "reservado_mensual": False, "hora_entrada": "2025-09-04 11:20", "tipo_vehiculo_estacionado": 4},
        {"id": 11, "patente": "", "tipo_slot": 3, "ocupado": False, "reservado_mensual": False, "hora_entrada": None, "tipo_vehiculo_estacionado": 0},  
        {"id": 12, "patente": "", "tipo_slot": 2, "ocupado": False, "reservado_mensual": True, "hora_entrada": None, "tipo_vehiculo_estacionado": 0} """
    ],

    # PISO 1 - 3x4 slots
    [
        [13, "", 2, False, False, None, 0],  
        [14, "", 1, False, False, None, 0],
        [15, "PQR678", 2, True, False, "2025-09-04 08:00",2], 
        [16, "", 4, False, False, None, 0],
        [17, "STU901", 1, True, False, "2025-09-04 09:30",1],
        [18, "", 3, False, True, None, 0],
        [19, "", 2, False, False, None, 0],   
        [20, "VWX234", 3, True, False, "2025-09-04 07:20", 3],
        [21, "", 1, False, False, None, 0],   
        [22, "", 4, False, False, None, 0],
        [23, "YZA567", 1, True, False, "2025-09-04 10:45",1], 
        [24, "", 2, False, False, None, 0]
    ],

    # PISO 2 - 3x4 slots
    [
        [25, "BCD890", 2, True, False, "2025-09-04 06:30",2], 
        [26, "", 1, False, False, None, 0],
        [27, "", 4, False, True, None, 0], 
        [28, "", 2, False, False, None, 0],
        [29, "", 3, False, False, None, 0], 
        [30, "EFG123", 4, True, False, "2025-09-04 12:00", 4],
        [31, "", 1, False, False, None, 0], 
        [32, "HIJ456", 2, True, False, "2025-09-04 08:45", 2],
        [33, "", 2, False, False, None, 0],  
        [34, "", 3, False, False, None, 0],
        [35, "", 1, False, False, None, 0],  
       # [36, "KLM789", 1, True, True, "2025-09-04 09:00", 1]
    ],

    # PISO 3 - 3x4 slots
    [
        [37, "", 4, False, False, None, 0],  
        [38, "", 2, False, False, None, 0],
        [39, "", 1, False, False, None, 0],  
        [40, "NOP012", 3, True, False, "2025-09-04 11:00", 3],
        [41, "", 2, False, True, None, 0],   
        [42, "QRS345", 2, True, False, "2025-09-04 07:00", 2],
        [43, "", 4, False, False, None, 0], 
        [44, "", 3, False, False, None, 0],
        [45, "TUV678", 1, True, False, "2025-09-04 10:15",1],
        [46, "", 1, False, False, None, 0],
        [47, "", 2, False, False, None, 0], 
        [48, "", 4, False, False, None, 0]
    ]
]

# Representacion costos posicion0: precio por hora posicion1 precio por dia

COSTOS = [
    [],  # vacio, seria el 0 que no representa nada,
    [2200, 50000],  # 1 moto
    [2400, 165000],  # auto
    [3500, 200000],  # camioneta
    [1000, 20000] #Bici
]