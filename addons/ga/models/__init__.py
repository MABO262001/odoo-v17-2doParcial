# Importa las clases de tus modelos
from . import estudiante
from . import profesor
from . import materia
from . import curso
from . import paralelo
from . import sucursal
from . import materia_profesor
from . import materia_profesor_horario
from . import horario
from . import gestion
from . import gestion_paralelo
from . import bloque
from . import piso
from . import subgestion
from . import parentesco
from . import apoderado
from . import inscripcion
from . import gestion_paralelo_materia_profesor_horario
from . import nota
from . import matricula
from . import aviso

# Expone las clases de tus modelos
Estudiante = estudiante.Estudiante
Profesor = profesor.Profesor
Materia = materia.Materia
Curso = curso.Curso
Paralelo = paralelo.Paralelo
Sucursal = sucursal.Sucursal
MateriaProfesor = materia_profesor.MateriaProfesor
MateriaProfesorHorario = materia_profesor_horario.MateriaProfesorHorario
Horario = horario.Horario
