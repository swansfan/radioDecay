import numpy as np

# function to simulate random decay
def simdecay(maxx_atoms, maxy_atoms, maxsteps, decay_constant):
    # Set up arrays with numbers of decayed and undecayed atoms for each step
    simatomsremaining = np.full(maxsteps+1,maxx_atoms*maxy_atoms,dtype='int')
    simatomsdecayed = np.zeros(maxsteps+1,dtype='int')

    # Set up array with undecayed atoms for each half sampleTime
    simatoms = np.ones((maxx_atoms, maxy_atoms, maxsteps + 1), dtype='int')

    # Set up array with random numbers to test against to see if atom has decayed
    randoms = np.random.rand(maxx_atoms, maxy_atoms, maxsteps + 1)
    # Set decay flag to 1 to make sure that no atoms will decay at initial time step
    randoms[:, :, 0] = 1.
    # Flag where decay occurs based on decay constant
    decay_flag = np.where(randoms >= decay_constant, 1, 0)
    for step in range(1, maxsteps+1):
        previous_step_atoms = simatoms[:, :, step - 1]
        current_step_atoms = simatoms[:, :, step]
        current_decays = decay_flag[:, :, step]
        current_step_atoms = current_step_atoms * current_decays * previous_step_atoms
        simatoms[:, :, step] = current_step_atoms
        simatomsremaining[step] = np.sum(simatoms[:, :, step])
        simatomsdecayed[step] = maxx_atoms * maxy_atoms - simatomsremaining[step]
    return simatoms, simatomsdecayed, simatomsremaining


# function to calculate analytical solution for exponential decay
def calcdecay(maxx_atoms, maxy_atoms, maxsteps, decay_constant):
    calctime = np.arange(0., float(maxsteps + 1), 0.1)
    calcdecay = float((maxx_atoms * maxy_atoms)) * np.exp(-decay_constant * time)
    return calctime, calcdecay

