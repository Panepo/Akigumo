def configLoader(file_path):
    parameters = {}
    try:
      with open(file_path, 'r') as file:
          for line in file:
              if line.strip() and not line.strip().startswith('#'):
                key, value = line.strip().split(' = ')
                parameters[key] = value
      return parameters
    except FileNotFoundError:
      raise FileNotFoundError
    except ValueError:
      raise ValueError

