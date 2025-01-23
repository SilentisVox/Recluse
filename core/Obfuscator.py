import random
import string
import os

class Obfuscator:
    # These functions will obfuscate a string

    # This method will turn each character to its ordinal value,
    # put it in a list, and convert each to a char and join it.
    def numbers_to_characters_to_string(self, command):
        command = command if isinstance(command, str) else command.group(0)[1:-1]

        numbers                         = []

        for character in command:
            numbers.append(str(ord(character)))

        numbers                         = ",".join(numbers)
        obfuscated_string               = "([string]::join('', ( ( " + numbers + " ) |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"

        return obfuscated_string

    # This method will turn each character to its ordinal value
    # and make a concatenate chain of the [char] method.
    def numbers_to_character_concatenate(self, command):
        command = command if isinstance(command, str) else command.group(0)[1:-1]

        numbers                         = []

        for character in command:
            oridnal_value               = str(ord(character))
            obfuscated_character        = f"[char]({oridnal_value})"
            numbers.append(obfuscated_character)

        obfuscated_string = "+".join(numbers)

        return obfuscated_string

    # This method is similar to the last. Instead of holding the
    # direct ordinal value, we do math before the [char] method.
    def numbers_to_character_concatenate_math(self, command):
        command = command if isinstance(command, str) else command.group(0)[1:-1]

        numbers                         = []
	
        for character in command:
            random_number               = random.randint(1, 99)
            operators                   = random.choice([("+", "-"), ("*", "/")])
            ordinal_value               = str(ord(character))
            obfuscated_character        = f"([char]({random_number}{operators[0]}{ordinal_value}{operators[1]}{random_number})" + "|%{$_}| % {$_} |%{$_})"
            numbers.append(obfuscated_character)

        obfuscated_string               = "+".join(numbers) 
	    
        return "+".join(numbers)

    # This method will take the string and scramble it.
    # The indices are remembered, so we can pull them out correctly.
    def random_string_to_string(self, command):
        command = command if isinstance(command, str) else command.group(0)[1:-1]

        characters_needed               = len(command) + 50
        character_positions             = [""] * characters_needed
        indices_used                    = []
    
        for character in command:
            unused_indices              = []

            for index in range(characters_needed):
                if character_positions[index] == "":
                    unused_indices.append(index)

            random_index                = random.choice(unused_indices)
            character_positions[random_index] = character
            indices_used.append(random_index)
        
        for index in range(len(character_positions)):
            if character_positions[index] == "":
                random_character        = random.choice(string.ascii_letters + string.digits)
                character_positions[index] =  random_character

        randomized_string               = "".join(character_positions)
        correct_indices                 = ",".join(map(str, indices_used))
        obfuscated_string               = f"('{randomized_string}'[{correct_indices}] -join '' " + "|%{$_}| % {$_})"

        return obfuscated_string

    # This method will take a string and convert each character
    # to a windows environment variable.
    def environment_variables_2_string(self, command):
        command = command if isinstance(command, str) else command.group(0)[1:-1]

        environment_variables           = [
            "ALLUSERSPROFILE",
	        "CommonProgramFiles",
	        "ComSpec",
	        "ProgramData",
	        "ProgramFiles",
	        "ProgramW6432",
	        "PSModulePath",
	        "PUBLIC",
	        "SystemDrive",
	        "SystemRoot",
	        "windir"
        ]

        environment_variable_character_map = {}

        for character in string.printable:
            environment_variable_character_map[character] = {}

            for variable in environment_variables:
                value                   = os.getenv(variable)

                if character in value:
                    environment_variable_character_map[character][variable] = []

                    for index, character_in_value in enumerate(value):

                        if character == character_in_value:
                            environment_variable_character_map[character][variable].append(index)
	    
        numbers                         = []

        for character in command:
            if character in environment_variable_character_map and environment_variable_character_map[character]:
                possible_variables      = list(environment_variable_character_map[character].keys())
                chosen_variable         = random.choice(possible_variables)
                possible_index          = environment_variable_character_map[character][chosen_variable]
                chosen_index            = random.choice(possible_index)
                obfuscated_character    = f"$env:{chosen_variable}[{chosen_index}]"
                numbers.append(obfuscated_character)
            else:
                other_functions         = [self.numbers_to_characters_to_string, self.numbers_to_character_concatenate, self.numbers_to_character_concatenate_math, self.random_string_to_string]
                other_function          = random.choice(other_functions)
                obfuscated_character    = other_function(character)
                numbers.append(obfuscated_character)

        obfuscated_string               = "(" + "+".join(numbers) + ")"

        return obfuscated_string

def test_obfuscator():
    obfuscator                          = Obfuscator()

    example                             = "iex \"get-help\""

    output1                             = obfuscator.numbers_to_characters_to_string(example)
    output2                             = obfuscator.numbers_to_character_concatenate(example)
    output3                             = obfuscator.numbers_to_character_concatenate_math(example)
    output4                             = obfuscator.random_string_to_string(example)

    print(output1, output2, output3, output4, sep="\n")

if __name__ == "__main__":
    test_obfuscator()