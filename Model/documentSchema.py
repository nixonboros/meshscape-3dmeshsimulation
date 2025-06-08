def create_document_schema(gen_name, size_x, size_y, max_z, 
                           smoothness, min_vx, max_vx, min_vy, 
                           max_vy, rock_den, bush_den, tree_den, 
                           log_den, stick_den, boulder_den):
    
    return {
        'GenName': gen_name,
        'SizeX': size_x,
        'SizeY': size_y,
        'MaxZ': max_z,
        'Smoothness': smoothness,
        'MinVX': min_vx,
        'MaxVX': max_vx,
        'MinVY': min_vy,
        'MaxVY': max_vy,
        'RockDen': rock_den,
        'BushDen': bush_den,
        'TreeDen': tree_den,
        'LogDen': log_den,
        'StickDen': stick_den,
        'BoulderDen': boulder_den
    }