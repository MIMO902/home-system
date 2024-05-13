import json

class Device:
    def __init__(self, ID, status, type, location):
        self.ID = ID
        self.status = status
        self.type = type
        self.location = location

    def toggleStatus(self):
        self.status = 'ON' if self.status == 'OFF' else 'OFF'

    def updateSettings(self, settings):
        pass  # To be overridden in child classes
    def __str__(self):
        return f"ID: {self.ID}, Type: {self.type}, Status: {self.status}, Location: {self.location}"

class Light(Device):
    def __init__(self, ID, status, type, location, brightness):
        super().__init__(ID, status, type, location)
        self.adjustBrightness(brightness)

    def adjustBrightness(self, level):
      if level < 100 and level > 0:
        self.brightness = level
        return True
      else:
        print("brightness level not valid")

    def updateSettings(self, settings):
        if 'brightness' in settings:
            level = settings['brightness']
            self.adjustBrightness(level)
            
    def __str__(self):
        return f"ID: {self.ID}, Type: {self.type}, Status: {self.status}, Location: {self.location}, brightness: {self.brightness}"

class Thermostat(Device):
    def __init__(self, ID, status, type, location, temperature):
        super().__init__(ID, status, type, location)
        self.setTemperature(temperature)

    def setTemperature(self, temp):
      if temp > 60 and temp < 80:
        self.temperature = temp
        return True
      else:
        return f"temprature degree is not valid"

    def updateSettings(self, settings):
        if 'temperature' in settings:
            temp = settings['temperature']
            self.setTemperature(temp)
            
    def __str__(self):
        return f"ID: {self.ID}, Type: {self.type}, Status: {self.status}, Location: {self.location}, temperature: {self.temperature} F"

class Camera(Device):
    def __init__(self, ID, status, type, location, angle):
        super().__init__(ID, status, type, location)
        self.adjustAngle(angle)

    def adjustAngle(self, newAngle):
      if newAngle > 0 and newAngle < 360:
        self.angle = newAngle
        return True
      else:
        return f"angle degree is not valid"

    def updateSettings(self, settings):
        if 'angle' in settings:
            self.angle = settings['angle']

    def __str__(self):
        return f"ID: {self.ID}, Type: {self.type}, Status: {self.status}, Location: {self.location}, Angle: {self.angle}"

class User:
    def __init__(self, UserID=None, Name=None, AccessLevel=None):
        self.UserID = UserID
        self.Name = Name
        self.AccessLevel = AccessLevel

    def authenticate(self):
        if self.AccessLevel == 'Admin':
         return True

    def sendCommand(self, command):
        pass  # To be implemented in Controller class
    def __str__(self):
        return f"User ID: {self.UserID}, Name: {self.Name}, Access Level: {self.AccessLevel}"


class Scheduler:
    def __init__(self):
        self.ScheduledTasks = []

    def addTask(self, task):
        self.ScheduledTasks.append(task)

    def removeTask(self, taskID):
        self.ScheduledTasks = [task for task in self.ScheduledTasks if task['taskID'] != taskID]

    def executeTasks(self):
        pass  # Placeholder for demo purposes


class Controller:
    def __init__(self,devices=None,users=None,device_id_counter=1,user_id_counter=1):
       if devices is None:
        self.Devices=[]
       else:
        self.Devices=devices
       if users is None:
        self.Users=[]
       else:
        self.Users=users
       self.user_id_counter = user_id_counter
       self.device_id_counter=device_id_counter

    def addDevice(self, device):
        self.Devices.append(device)

    def removeDevice(self, deviceID):
        self.Devices = [device for device in self.Devices if device.ID != deviceID]
        print("device deletes successfully")

    def getUserCommands(self, userID, action, deviceID=None, settings=None):
        user = next((user for user in self.Users if user.UserID == userID), None)
        device = next((device for device in self.Devices if device.ID == deviceID), None)
        if device:
          if user.authenticate() and action == 'control device':
            device.toggleStatus()
            print("User",user.UserID,"changed the state of", device.type,"device",device.ID,".")
          elif user.authenticate() and action == 'modify settings':
            if device.type.lower() =='camera':
              settings={'angle':settings}
            elif device.type.lower()=='light':
              settings={'brightness':settings}
            else:
              settings={'temperature':settings}
            done=device.updateSettings(settings)
            if done:
              print( "User", user.UserID," modified settings of ",device.type," device ",device.ID,".")
            else:
              print("Error")  
          elif action == 'view device':
            print(device)
          else:
            print("Access denied.")
        else:
          print("Device not found.")

scheduler = Scheduler()
controller = Controller()

def saveUsersToFile(filename):
  with open(filename, 'w') as file:
    user_data = [{'UserID': user.UserID, 'Name': user.Name, 'AccessLevel': user.AccessLevel} for user in controller.Users]
    json.dump(user_data, file)

def saveDevicesToFile(filename):
  with open(filename, 'w') as file:
    device_data = [{'ID': device.ID, 'status': device.status, 'type': device.type, 'location': device.location,
      'brightness': getattr(device, 'brightness', None), 'temperature': getattr(device, 'temperature', None),
      'angle': getattr(device, 'angle', None)} for device in controller.Devices]
    json.dump(device_data, file)

def loadUsersFromFile(filename,):
  with open(filename, 'r') as file:
    user_data = json.load(file)
    controller.Users = [User(data['UserID'], data['Name'], data['AccessLevel']) for data in user_data]
    controller.user_id_counter = max([user.UserID for user in controller.Users]) + 1 if controller.Users else 1

def loadDevicesFromFile(filename):
  with open(filename, 'r') as file:
    device_data = json.load(file)
    for data in device_data:
      if data['type'].lower() == 'light':
        device = Light(data['ID'], data['status'], data['type'], data['location'], data['brightness'])
      elif data['type'].lower() == 'thermostat':
        device = Thermostat(data['ID'], data['status'], data['type'], data['location'], data['temperature'])
      elif data['type'].lower() == 'camera':
        device = Camera(data['ID'], data['status'], data['type'], data['location'], data['angle'])
      else:
        continue  # Skip invalid device types

      controller.addDevice(device)
      controller.device_id_counter = max(controller.device_id_counter, device.ID) + 1

def createDevice(stat,type, settings, location):
  if type.lower() == 'light':
    device = Light(controller.device_id_counter, stat, type, location, settings['brightness'])
  elif type.lower() == 'thermostat':
    device = Thermostat(controller.device_id_counter, stat, type, location, settings['temperature'])
  elif type.lower() == 'camera':
    device = Camera(controller.device_id_counter, stat, type, location, settings['angle'])

  controller.addDevice(device)
  controller.device_id_counter += 1
  print(type.capitalize()," device created with ",settings," in the",location,".")

def createUser(name, access_level):
  user = User(controller.user_id_counter, name, access_level)
  controller.Users.append(user)
  controller.user_id_counter += 1
  print("User",name, "with ID",user.UserID,"and",access_level,"access level created successfully.")

def DeleteUser(userID):
  controller.Users = [user for user in controller.Users if user.UserID != userID]
  print("user deleted successfully")

def scheduleEvent(time, device_id, action):
  task = {'time': time, 'device_id': device_id, 'action': action, 'taskID': len(scheduler.ScheduledTasks) + 1}
  scheduler.addTask(task)
  return f"Event scheduled at {time} to {action} device {device_id}."

def executeScheduledEvents():
  scheduler.executeTasks()
  return "Executed scheduled events successfully."



loadUsersFromFile('users.json')
loadDevicesFromFile('devices.json')
        
user=User()        
choice = input("1:create user   2:login  q:to exit \n")
while choice != 'q':
  if choice == '1':
    name = input("Name: ")
    access= input("1:Admin 2:guest")
    if access == '1':
      createUser(name,'Admin')
    elif access == '2':
      createUser(name,'Guest')
    else:
      print("invalid input")
    user = next((user for user in controller.Users if user.UserID == controller.user_id_counter-1), None)
  elif choice == '2':
    ID=int(input("ID : "))
    user = next((user for user in controller.Users if user.UserID == ID), None)
    if user:
      print("loged in successfully")
    else:
      print("invalid ID")
  else:
    print("invalid input")
  if user.AccessLevel == 'Admin':
    choice2=input("\n\n\n1:Add user \n2:Delete user \n3:Add device \n4:Delete device \n5:Edit device \n6:view device \nb:to go back \nq:to exit\n")
    while choice2 != 'b':
      if choice2 == '1':
        name=input("user name : ")
        access= input("1:Admin 2:guest")
        if access == '1':
          createUser(name,'Admin')
        elif access == '2':
          createUser(name,'Guest')
        else:
          print("invalid input")
      elif choice2 == '2':
        ID=int(input("user ID : "))
        DeleteUser(ID)
      elif choice2 == '3':
        type = input("1:light \n2:thermostate \n3:camera \nchoose device type : ")
        if type == '1':
          type='light'
          sett=int(input("Enter brightness settings : "))
          sett={'brightness': sett}
        elif type == '2':
          type='thermostat'
          sett=int(input("Enter temprature settings : "))
          sett={'temperature': sett}
        elif type=='3':
          type='camera'
          sett=int(input("Enter adjustment settings : "))
          sett={'angle': sett}
        else:
          print("invalid input")
        stat=input("1 : ON  2:OFF")
        if stat=='1':
          stat='ON'
        elif stat=='2':
          stat="OFF"
        else:
          print("invalid input")
        loc=input("Enter the location of the device : ")
        createDevice(stat,type,sett,loc)
      elif choice2=='4':
        ID=int(input("Enter ID : "))
        controller.removeDevice(ID)
      elif choice2=='5':
        choice3 = input("1:control device  \n2:modify device\n")
        if choice3=='1':
          ID=int(input("device ID : "))
          controller.getUserCommands(user.UserID,'control device',ID)
        elif choice3=='2':
          ID=int(input("device ID : "))
          sett=int(input("settings : "))
          controller.getUserCommands(user.UserID,'modify settings',ID,sett)
        else:
          print("invalid input")
      elif choice2=='6':
        ID=int(input("device ID : "))
        controller.getUserCommands(user.UserID,'view device',ID)
      elif choice2=='q':
        break
      else:
        print("invalid input")
      choice2=input("\n\n\n1:Add user \n2:Delete user \n3:Add device \n4:Delete device \n5:Edit device \n6:view device \nb:to go back \nq:to exit \n")        
  else:
    choice2=input("1:view device \nb:go back \nq:exit \n")
    while choice2 != 'b':
      if choice2=='1':
        ID=int(input("device ID : "))
        controller.getUserCommands(user.UserID,'view device',ID)
      elif choice2=='q':
        break
      else:
        print("invalid input")
      choice2=input("1:view device \nb:go back \nq:exit")  
  if choice2 != 'q':  
    choice = input("\n\n\n1:create user   2:login  q:to exit")
  else:
    choice = 'q'

saveUsersToFile('users.json')
saveDevicesToFile('devices.json')

# for user in controller.Users:
#   print(user)  # Print loaded users

# for device in controller.Devices:
#   print(device)  # Print loaded devices
        
        
        
        
        
        