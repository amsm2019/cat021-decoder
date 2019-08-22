
class Mess(object):
    def __init__(self,parsed):
        self.parsed = parsed
        pass
    def getData(self):
        self.getFlightID()
        self.getPosition()
        self.getAltitude()
        self.getAngle()
        self.getGroundSpeed()
        self.getTAddr()

    # Flightid
    # Data Item I021/170, Target Identification
    def getFlightID(self,byte_mess=''):
        if 'I170' in self.parsed[0]:
            self.flight = self.parsed[0]['I170']['TId']['val']
        else:
            self.flight = ""
        return 
    # 经纬度 I131
    # (Latitude) Range -90 ≤ latitude ≤ 90 deg.
    # (Longitude) Range -180 ≤ longitude < 180 deg.
    def getPosition(self,str_mess=None):
        if 'I131' in self.parsed[0]:
            self.lat = self.parsed[0]['I131']['Lat']['val']
            self.lon = self.parsed[0]['I131']['Lon']['val']
        else:
            self.lat = -1
            self.lon = -1
        pass
    # 高度 I140
    # -1500 ft <= Altitude <= 150000 ft 
    # (LSB) = 6.25 ft
    def getAltitude(self,str_mess=None):
        if 'I140' in self.parsed[0]:
            self.altitude = self.parsed[0]['I140']['geometric_height']['val']
        else:
            self.altitude = -1
        pass
    # 地速  
    # LSB = 2^-14NM/s 
    def getGroundSpeed(self,str_mess=None):
        if 'I160' in self.parsed[0]:
            self.speed = int(self.parsed[0]['I160']['GS']['val']  * 3600) # 1 knot
        else:
            self.speed = -1
        pass
    # Track Angle
    # Track Angle clockwise reference to “True North”
    def getAngle(self,str_mess=None):
        if 'I160' in self.parsed[0]:
            self.track = self.parsed[0]['I160']['TA']['val']
        else:
            self.track = -1
        pass  
        
    # Target Address
    def getTAddr(self,str_mess=None):
        if 'I080' in self.parsed[0]:
            self.hex = self.parsed[0]['I080']['TAddr']['val']
        else:
            self.hex = ''
        pass

