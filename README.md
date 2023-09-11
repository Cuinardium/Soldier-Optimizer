#TP2 SIA - Algoritmos Géneticos

Este repositorio contiene un programa que simula la evolucion de una poblacion de soldados en busca de conseguir el mejor soldado para clase mediante el uso de algoritmos geneticos.  La simulacion desarrollada es altamente configurable mediante el archivo `config.json`. 

## Configuracion
El archivo `config.json` sigue el siguiente formato:
```json
{
    "test_name": "test1",
    "iterations": 10,

    "character_class": "warrior" | "archer" | "defender" | "infiltrator",

    "population_size": 100,

    "selection": {
        "method1": "elitism" | "roulette" | "universal" | "boltzmann" | "ranking" | "tournament",
        "method1_proportion": 0.5,
        "method2": "roulette",
        "amount": 100,
        "boltzmann": {
            "temperature": 100
        },
        "tournament": {
            "size": 10,
            "probabilistic": true,
            "threshold": 0.75
        }
    },

    "crossover": {
        "method": "anular" | "point" | "two_point" | "uniform",
        "uniform": {
            "crossover_probability": 0.5
        }
    },

    "mutation": {
        "probability": 1,
        "uniform": true,
        "multi_gen": true,
        "single_gen": {
            "gen_to_mutate": "strength" | "agility" | "expertise" | "resistance" | "health" | "height"
        },
        "non_uniform": {
            "descent_rate": 0.5
        }
    },

    "replacement": {
        "method1": "universal",
        "method1_proportion": 0.2,
        "method2": "boltzmann",
        "amount": 100,
        "boltzmann": {
            "temperature": 100
        },
        "tournament": {
            "size": 2,
            "probabilistic": false,
            "threshold": 0.75
        }
    },

    "stop_criteria": {
        "criteria": "generations" | "fitness" | "fitness_convergence" | "structure_convergence",
        "generations": {
            "max_generations": 100
        },
        "fitness": {
            "expected_fitness": 50
        },
        "fitness_convergence": {
            "fitness_delta": 0.001,
            "similar_generations_threshold": 10
        },
        "structure_convergence": {
            "similar_generations_threshold": 10,
            "similar_individuals_proportion": 1,
            "deltas": { 
                "strength": 0.01,
                "agility": 0.01,
                "expertise": 0.01,
                "resistance": 0.01,
                "health": 0.01,
                "height": 0.01
            }
        }
    }
}

```

Donde se puede configurar cada seccion del programa

### Opciones generales
Configuran parametros generales del programa
- **test_name**: El nombre del directorio donde se guardaran los resultados. Si **test_name** es _"test1"_ , los resultados se guardaran en el directorio `results/test1`.
- **iterations**: La cantidad de veces que se corre la simulacion, debido a la naturaleza estocastica de los algoritmos se recomienda correr varias veces las simulaciones.
- **character_class**: El tipo de soldado con la que correr la simulacion estos pueden ser _warriors_, _archer_, _defender_ e _infiltrator_. Cada tipo de soldado prioritizara un tipo de caracteristicas ante otras
- **population_size**:  La cantidad de soldados que habra por generacion, esta cantidad es fija.

### Selection
Configura de que manera se seleccionan los individuos para la etapa de cruza. Es posible configurar una seleccion donde un porcentaje se elijan con un metodo y el resto con otro.
- **method1**: El  primer metodo a usar, se pueden elegir _elitism_, _roulette_, _universal_, _boltzmann_,  _ranking_ y _tournament_
- **method2**: El segundo metodo a usar, se pueden elegir los mismos metodos que el 1.
- **method1_proportion**: El porcentaje de individuos a elegir con el metodo1.
- **amount**: La cantidad de individuos a elegir, debe ser menor a **population_size**

Algunos metodos de eleccion tienen configuraciones adicionales

#### Boltzmann
**temperature**: La temperatura inicial del metodo de boltzmann
#### Tournament
- **size**: El tamano de cada torneo
- **probabilistic**: Flag donde se especifica si se debe usar un torneo determinista o probabilistico
- **threshold**: La probabilidad de que se elija el individuo que gana el torneo
### Crossover
Configura de que manera se realiza la cruza entre dos individuos.
- **method**: El metodo de cruza a utilizar, pueden ser los siguientes: _anular_, _point_, _two_point_ y _uniform_.
#### Uniform
El metodo uniform tiene un parametro especial:
- **crossover_probability**: la probabilidad de que se realize la cruza de un gen
### Mutation
Configura de que manera se realiza la mutacion de los nuevos individuos:
- **probabilty**: La probabilidad de que un individuo mute
- **uniform**: Flag que especifica, si la probabilidad debe ser constante o reducirse con las generaciones. La cadencia con la que esta probabilidad desciende se especifica con **descent_rate**
- **multi_gen**: Flag que especifica si se debe mutar un solo gen o todos los genes. De ser falso, se especifica que gen mutar con **gen_to_mutate**, este puede ser _strength_, _agility_, _expertise_,  _resistance_, _health_ y _height_. 
### Replacement
Configura de que manera se eligiran los individuos para la siguiente generacion. Los parametros son los mismos que en la seccion de _selection_. Se recomienda que _amount_ sea igual a _population_size_ para que la poblacion sea constante.

### Stop Criteria
Configura bajo que condicion terminara la simulacion
- **criteria**: Especifica la condicion a usar, esta puede ser _generations_, _fitness_, _fitness_convergence_ y _structure_convergence_. Cada una de estas son configurables con sus parametros.
#### Generations
Especifca el numero de generaciones a producir. 
- **max_generations**: El numero de generaciones a producir
#### Fitness
Especifica el nivel de _fitness_ bajo el que cortar.
- **expected_fitness**: El nivel de _fitness_ al que se busca llegar.
#### Fitness Convergence
Se corta si se determina que se ha llegado a una convergencia del nivel de _fitness_
- **fitness_delta**: La diferencia de _fitness_ bajo el que se determina que una generacion y otra tienen un nivel similar de fitness
- **similar_generations_threshold**: Cuantas generaciones seguidas deben tener un nivel similar de _fitness_ para que se determine que se ha llegado a una convergencia
#### Structure Convergence
Se corta si se determina que se ha llegado a una convergencia en cuanto a la similitud de caracteristicas entre generaciones.
- **similar_generations_threshold**:  Cuantas generaciones similares seguidas deben ocurrir para que se determine que se ha llegado a una convergencia
- **similar_individuals_proportion**: La proporcion de individuos similares que debe haber entre dos generaciones para que estas se consideren similares.
- **deltas**: Especifica la diferencia entre cada gen para que estos se consideren similares entre dos individuos, para que dos individuos se consideren similares todas los genes especificados deben ser similares. No es necesario que se especifiquen todos los genes, si se quiere ignorar un gen para el calculo de similitud se puede borrar su delta del archivo.
## Ejecucion
Para ejecutar el programa basta con correr `python main.py` desde la raiz del proyecto. Una vez corrido el programa se realizara la simulacion correspondiente a la configuracion dada y se guardaran los resultados en el directorio `results/[test_name]` en un archivo csv, tambien se guardara una copia del archivo de configuracion.
