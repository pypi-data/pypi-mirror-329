import winreg

class RegistryEditor:
    def __init__(self, key_path, value_name, registry_type=winreg.REG_SZ):
        self.key_path = key_path
        self.value_name = value_name
        self.registry_type = registry_type

    def create_key(self):
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
            winreg.CloseKey(key)
            # print(f"Successfully created key: {self.key_path}")
        except WindowsError as e:
            print(f"Error creating key: {e}")

    def set_value(self, value):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, self.value_name, 0, self.registry_type, value)
            winreg.CloseKey(key)
            # print(f"Successfully set value: {value}")
        except WindowsError as e:
            print(f"Error setting value: {e}")

    def get_value(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ)
            value, reg_type = winreg.QueryValueEx(key, self.value_name)
            winreg.CloseKey(key)
            # print(f"Successfully got value: {value}")
            if value is None:
                value = ""
            return value
        except WindowsError as e:
            print(f"Error getting value: {e}")
            return None

    def delete_value(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, self.value_name)
            winreg.CloseKey(key)
            # print(f"Successfully deleted value: {self.value_name}")
        except WindowsError as e:
            print(f"Error deleting value: {e}")

    def delete_key(self):
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.key_path)
            # print(f"Successfully deleted key: {self.key_path}")
        except WindowsError as e:
            print(f"Error deleting key: {e}")

# 使用例子
# editor = RegistryEditor(r"Software\ledTest", "licKey", winreg.REG_SZ)
# editor.create_key()
# editor.set_value("0d025be32f248935axzafa0d5a24ec14de")
# value = editor.get_value()


# editor = RegistryEditor(r"Software\ledTest", "mCodeType", winreg.REG_SZ)
# editor.create_key()
# editor.set_value("0d025be32f248935axzafa0d5a24ec14de")
# print(value)
# editor.delete_value()
# editor.delete_key()