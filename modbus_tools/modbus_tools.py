from asyncio.base_subprocess import ReadSubprocessPipeProto
import json
import os
from datetime import datetime
import time
import struct
from typing import Any, Dict, List, cast
from numpy import true_divide
from pyModbusTCP.client import ModbusClient
import pkg_resources

from modbus_tools.utils import MetterTypes

class ModbusConfig:
    """ Clase para definir la configuracion de cliente modbus
    """

    def read_raw_file(self, path: str) -> str:
        try:
            with open(path, 'r') as f:
                content = f.read()
                f.close()
        except (FileNotFoundError, IOError) as e:
            #traceback.print_exc(file=sys.stdout)
            #print(str(e))
            raise(e)
        return content

    def read_json_file(self, path: str) -> dict:
        try:
            return json.loads(self.read_raw_file(path))
        except Exception as e:
            #traceback.print_exc(file=sys.stdout)
            #print(str(e))
            raise(e)

    def conf_from_json(self, path):
        """ Reads 'app_conf.json' from specified path.

        Args:
            path (str): path to app_conf.json
        """

        # path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './app_conf.json')
        info = self.read_json_file(path)
        modbus_info = cast(dict, info['modbus'])

        self.__host = modbus_info['host']
        self.__port = modbus_info['port']
        self.__slave = modbus_info['slave']
        self.__metter_type = modbus_info['metter_type']

        stream = pkg_resources.resource_stream(__name__, f'data/{self.__metter_type}.json')
        # json_string = stream.read().decode()
        self.__registers = json.load(stream)
        
    def __init__(self, path_to_json):
        self.__host = "default"
        self.__port = 0
        self.__slave = 0
        self.__metter_type = "default"

        self.conf_from_json(path_to_json)
    
    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def slave(self):
        return self.__slave

    @property
    def metter_type(self):
        return self.__metter_type

    @property
    def registers(self):
        return self.__registers

    @property
    def example_app_conf(self):
        """ Ejemplo de formato para archivo app_conf.json

        Returns:
            (dict): ejepmlo del contenido del archivo app_conf.json
        """
        
        example_conf = {
            "modbus": {
                "host": "169.254.249.248",
                "port": 502,
                "slave": 159,
                "metterType": "G4"
            }
        }

        print(json.dumps(example_conf, indent=4))

        return example_conf

class RegReadResponse:
    """ Es una clase auxiliar para dar formato de objeto a un peticion de modbus
    """

    @property
    def name(self):
        """ Propiedad que devuelve el nombre de la variable solicitada

        Returns:
            string: Devuelve el nombre
        """
        return self._name

    @property
    def unit(self):
        """ Propiedad que devuelve la unidad de la variable solicita

        Returns:
            str: Devuelve la unidad
        """
        return self._unit

    @property
    def value(self):
        """ Propiedad que devuelve el valor leído por modbus

        Returns:
            float: Valor de lectura de modbus
        """
        return self._value

    # Constructor que asigna los valores a las variables internas
    def __init__(self, name: str, unit: str, value: float) -> None:
        """ Constructor de classes

        Args:
            name (str): Nombre del registro
            unit (str): Unidad de medida del registro
            value (float): Valor de lectura del registro
        """
        self._name = name
        self._unit = unit
        self._value = value

    # Representacion del objeto en forma 'string'
    def __repr__(self) -> str:
        """ Representacion del objeto en forma 'string'
        """
        return f"<ModbusReg('name={self.name}', unit='{self.unit}', value={self.value})>"

class JsonModbusClient_R(ModbusClient):
    """Clase que hereda de 'ModbusClient', implementa lectura de registros a partir de 'json'
    """

    @property
    def registers(self):
        return self._registers

    def __init__(self, metter_type, **kwargs):
        super().__init__(**kwargs)
        self.metter_type = metter_type

        self._registers = json.load(pkg_resources.resource_stream(__name__, f'data/{self.metter_type}.json'))

        self._registers_to_read = None

    @classmethod
    def from_app_conf(cls, app_conf_path:str):
        """ 'classmethod' para construir a partir del path a 'app_conf'. 
        JsonModbusClient_R crea el objeto 'ModbusConfig' e inicia el cliente
        con el host, port y slave_port cotenidos en app_conf.json.

        Args:
            app_conf_path (str): path del archivo app_conf.json
        """

        modbus_conf = ModbusConfig(app_conf_path)

        return cls(metter_type = modbus_conf.metter_type, host = modbus_conf.host, port = modbus_conf.port, unit_id = modbus_conf.slave, auto_open = True)

    def check_client_response(self):
        """ Comprueba que el cliente modbus responda.

        Returns:
            bool: True if response is ok , False if not
        """
        
        if (self.metter_type == MetterTypes.G4.name):

            regs_resp = self.read_input_registers(2283, 2) # modbus_code: 2283 corresponde al voltage PRM_CODE_AVG_V1_RMS

            if (regs_resp == None):
                return False
            elif (type(regs_resp[0]) == int):
                return True
            
        elif (self.metter_type == MetterTypes.PBB.name):

            regs_resp = self.read_input_registers(0, 2) # modbus_code: 0 corresponde al voltage "1/2 cycle RMS V1N of feeder 1 Average refresh every 1 min"

            if (regs_resp == None):
                return False
            elif (type(regs_resp[0]) == int):
                return True
        else:
            print("Tipo de medidor incorrecto ...")

    def read_from_json(self, jlist: List[dict]) -> List[RegReadResponse]:
        """ Realiza una consulta a un dispositivo modbus, y parsea la salida a una lista de RegReadResponse

        Args:
            jlist (List[dict]): Lista de registros a parsear. La lista debe estar en orden ascendente respecto a la propiedad start_reg

        Returns:
            List[RegReadResponse]: Lista de registros parseados resultado de la lectura de modbus
        """
        
        if len(jlist) < 1:
            return None

        # Register math (find first and last register)
        start_register = jlist[0]
        end_register = jlist[-1]
        start_read = start_register['memory_block_adress']
        end_read = end_register['memory_block_adress']
        # Number of registers to read
        regs2read = int((end_read - start_read) + (end_register['memory_block_size'] / 2))
        # Register's adress, type and name; stored in dictionaries
        target_regs = [entry.get('memory_block_adress') for entry in jlist]
        target_types = [entry.get('value_type') for entry in jlist]
        target_names = [entry.get('name') for entry in jlist]
        target_units = [entry.get('unit') for entry in jlist]
        target_regs_types = dict(zip(target_regs, target_types))
        target_regs_names = dict(zip(target_regs, target_names))
        target_regs_units = dict(zip(target_regs, target_units))

        # Leer registros
        regs_resp = self.read_input_registers(start_register['memory_block_adress'], regs2read)
        # Store the exact adresses of the readed registers
        readed_regs = list(range(start_read, start_read + regs2read))

        if regs_resp is None:
            return None

        # Diccionario con datos de salida
        reg_response = dict(zip(readed_regs, regs_resp))

        # Response list
        ret_list = []
        for target_key in target_regs_types:
            value = self.ProcessResponse(reg_response[target_key], target_regs_types[target_key])
            ret_list.append(RegReadResponse(target_regs_names[target_key], target_regs_units[target_key], value))

        return ret_list 

    def ProcessResponse(self, response_reg: Any, response_type: str) -> float or int:
        """Process each response, applies parsing if response is float

        Args:
            response_reg (register value): output from .read_input_registers()
            response_type (string): string stating the type of the response_reg ('float' or 'int')

        Returns:
            parsed_response: [float] or [int] depending on 'response_type' argument
        """
        if response_type == "float" or response_type == "double":
            parsed_response = self.ParseFloat(response_reg)
        # elif response_type == "double":
        #     parsed_response = self.ParseDouble(response_reg)
        elif response_type == "int":
            # falta definir la manera correcta de parsear enteros
            parsed_response = response_reg #self.ParseInt(response_reg)
        else:
            print("[EG4KModbusClient]: ProcessResponse(): ERROR")
            return None

        return parsed_response

    def ParseFloat(self, input) -> float:
        """ Parses a response into a float

        Args:
            input (register value): output from .read_input_registers()

        Returns:
            float: parsed float
        """
        str_input = f"{input:x}".ljust(8, '0')
        bytes_input = bytes.fromhex(str_input)

        float_number = struct.unpack('!f', bytes_input)[0]

        # print(f"[modbus_tcp.py]: ParseFloat(): {float_number}")
        return float_number

    def sort_regs_to_read(self, regsToRead):
        """ Simple 'bubble sort' from: https://realpython.com/sorting-algorithms-python/#the-bubble-sort-algorithm-in-python

        Args:
            array (list(str)): unsorted array

        Returns:
            list(str): sorted array
        """

        n = len(regsToRead)

        for i in range(n):
            # Create a flag that will allow the function to
            # terminate early if there's nothing left to sort
            already_sorted = True

            # Start looking at each item of the list one by one,
            # comparing it with its adjacent value. With each
            # iteration, the portion of the array that you look at
            # shrinks because the remaining items have already been
            # sorted.
            for j in range(n - i - 1):
                
                ind = j
                ind_adjacent = j + 1

                reg = list(filter(lambda r: r['name'] == regsToRead[ind], self._registers))
                if len(reg) > 1:
                    print('ERROR en modbus_tools/utils.py / sort_regs_to_read()')
                regInd = reg[0]['memory_block_adress']
                reg_adjacent = list(filter(lambda r: r['name'] == regsToRead[ind_adjacent], self._registers))
                if len(reg_adjacent) > 1:
                    print('ERROR en modbus_tools/utils.py / sort_regs_to_read()')
                regInd_adjacent = reg_adjacent[0]['memory_block_adress']

                if regInd > regInd_adjacent: # regsToRead[ind] > regsToRead[ind_adjacent]:
                    # If the item you're looking at is greater than its
                    # adjacent value, then swap them
                    regsToRead[ind], regsToRead[ind_adjacent] = regsToRead[ind_adjacent], regsToRead[ind]

                    # Since you had to swap two elements,
                    # set the `already_sorted` flag to `False` so the
                    # algorithm doesn't finish prematurely
                    already_sorted = False

            # If there were no swaps during the last iteration,
            # the array is already sorted, and you can terminate
            if already_sorted:
                break

        return regsToRead

    def set_regs_to_read(self, registerToRead):
        
        sorted_regs_to_read = self.sort_regs_to_read(registerToRead)

        self._registers_to_read = optimize_read(sorted_regs_to_read, self._registers)

    def read_registers(self, counter:int=25):

        output = []

        for register_group in self._registers_to_read:
            for i in range(counter):

                response = self.read_from_json(register_group)
                if response != None:

                    # print readed registers in a 'human readable' list
                    for item in response:
                        print(item)

                    output.extend(response)
                    break


        return output

    def read_harmonics(self):
        """ Funcion para leer los harmonicos
        """

        if self.metter_type == MetterTypes.G4.name:

            register_names = ['hI1_T', 'hI2_T', 'hI3_T']
            harmonics = []
            registers_to_read = 100
            starting_index_name = 1

            for name in register_names:

                reg_ = list(filter(lambda r: r['name'] == name, self._registers))

                if len(reg_) > 1:
                    print("WARNING [len(reg_) > 1] read_harmonics()")

                reg = reg_[0]

                # set the reference to 'memory_block_adress' ?, this reference is stored in register 2441 ?
                armonics_code_written = self.write_single_register(2441, reg['memory_block_adress'])

                if (armonics_code_written == True):

                    response = self.read_input_registers(2442, registers_to_read)

                    if (response != None):
                        
                        if (len(response) > 0):

                            for i in range(len(response)):
                                if (i%2 == 0):
                                    harmonics.append(RegReadResponse(name[:3]+f"_{int(starting_index_name+i/2)}", 'null', self.ParseFloat(response[i])))

                elif (armonics_code_written == None):
                    print(f"ERROR Response while writing modbus code: {reg['memory_block_adress']} for reg: {reg['name']} for G44XX metter.")
                    
        elif self.metter_type == MetterTypes.PBB.name:

            register_names = ['hI1_0', 'hI3_0', 'hI2_0']
            harmonics = []
            registers_to_read = 102
            starting_index_name = 0

            for name in register_names:

                reg_ = list(filter(lambda r: r['name'] == name, self._registers))

                if len(reg_) > 1:
                    print("WARNING [len(reg_) > 1] read_harmonics()")

                reg = reg_[0]

                response = self.read_input_registers(reg['memory_block_adress'], registers_to_read)

                if (response != None):
                    if (len(response) > 0):

                        for i in range(len(response)):
                            if (i%2 == 0):
                                harmonics.append(RegReadResponse(name[:3]+f"_{int(starting_index_name+i/2)}", 'null', self.ParseFloat(response[i])))
            
        for item in harmonics:
            print(item)

        return harmonics

class JsonModbusClient_RW(JsonModbusClient_R):
    """Clase que hereda de 'JsonModbusClient_R', añade escritura de registros a partir de 'json'
    """

    def write_register(self, register: dict, value: Any) -> bool:
        """Realiza escritura de registros modbus

        Args:
            register (dict): registro a escribir
            value (Any): valor a escribir

        Returns:
            bool: true o false dependiendo si pudo escribir o no
        """
        
        stop_flag = False
        while not stop_flag:
            write_resp = self.write_single_register(register['start_reg'], value)
            if write_resp:
                print(f"[modbus_tcp.py]: write_from_json(): {register['name']} Written successfully!")
                stop_flag = True
            elif not write_resp:
                print(f"[modbus_tcp.py]: write_from_json(): {register['name']} Error while writing...")
                stop_flag = True
                break
            else:
                print(f"[modbus_tcp.py]: write_from_json(): unknown error")
                stop_flag = True

        return write_resp

def optimize_read(registers_name: list[str], all_registers: list[dict], max_step: int = 30) -> list[dict]:
    """Optimiza la lectura de registros permitiendo un maximo de consultas seguidas

    Args:
        registers_name (List[str]): Nombre de registros
        all_registers (List[dict]): Registros a buscar
        max_step (int, optional): Tamaño maximo de bloque de lectura. Defaults to 30.

    Returns:
        List[dict]: Lista de registros agrupada por su cercania
    """

    ret_list = []
    aux_list = []
    start_reg = {}
    for i, reg_name in enumerate(registers_name):
        register_search = list(filter(lambda r: r['name'] == reg_name, all_registers))

        if len(register_search) < 1:
            continue

        register = register_search[0]

        if len(aux_list) == 0:
            start_reg = register

        #TODO: ¿usar una diferencia fija en vez del block_size?, NO TODOS LOS REGISTROS TRAEN ESPECIFICADO EL BLOCK SIZE
        difference = (register['memory_block_adress'] + register['memory_block_size']) - start_reg['memory_block_adress']

        if difference < max_step:
            aux_list.append(register)
            if i == (len(registers_name) - 1):
                ret_list.append(aux_list)
            continue

        ret_list.append(aux_list)
        aux_list = []
        aux_list.append(register)
        start_reg = register

        # si no 'cupo' y ya es la ultima iteracion, agregar el registro actual return list
        if i == (len(registers_name) - 1):
            ret_list.append(aux_list)
        
    return ret_list

def JsonModbus_WriteManager(json_modbus_client_rw:JsonModbusClient_RW, registers:list, values:list, counter:int=25) -> dict:
    """Escribe multiples registros de modbus por bloques

    Args:
        json_modbus_client_rw (JsonModbusClient_RW): Cliente modbus con funciones de escritura
        registers (List): Registros a escribir
        values (List): Valores a escribir
        counter (int, optional): Contador de intentos. Defaults to 25.

    Returns:
        dict: Indicador si el registro se escribio
    """

    output = {}

    for i in range(len(registers)):

        response = None
        counterBreak = 0

        print('[main_functions.py]:')
        print(f'... Register to write: {registers[i]}')
        print(f'... Value to write: {values[i]}')

        while response != True:

            # .write_register() devuelve 'bool' o 'None' si logra escribir o no,
            # en especifico dentro de su codigo se define: " return True if is_ok else None "
            response = json_modbus_client_rw.write_register(registers[i], values[i])
            if response == True:
                print(f'... ... Register written: {values[i]}')
                output[registers[i]['name']] = response

            counterBreak += 1
            if counterBreak > counter:
                print(f'... ... WARNING!: Write attempts limit reached, Regisger not written!: {registers[i]}')
                break

            time.sleep(0.2)

    return output
