import rhinoscriptsyntax as rs

with open("D:\Points3D.txt", 'r') as f:
    for line in f.readlines():
        line = line.split(' ')
        x = float(line[0][1:])
        y = float(line[1][1:])
        z = float(line[2][1:])
        c = line[3][3:]
        
        if '_' in c:
            color = rs.CreateColor([255, 0, 0])
        else:
            c = float(c)
            color = rs.CreateColor([c, c, c])
        print x, y, z, color
        
        pt = rs.AddPoint(x, y, z)
        rs.ObjectColor(pt, color)
