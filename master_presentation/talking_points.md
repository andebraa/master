0
Predicting static friction in a molecular dynamic system using machine learning
-> interjunctional asperities

---

In my thesis we studied microscopic friction in a system in which we varied the asperity placements to observe the effects of asperity interactions on the static friction
- multi scale effects of asperities makes friction complicated.
- wish to study effects of varying asperity configurations.

---
1
Introduction to friction -> WHY IS IT IMPORTANT TO STUDY
molecular dynamics -> how do we model friction
analysis -> machine learning
results 
---
2
Friciton is immensly important. 
whether the concern is moving or still objects, energy loss, heat transfer or wear and tear
friction plays a role in near everything we do.

It also spans across multiple, if not all, natural sciences, 
biology, geology, mathematics, chemistry etc etc

-interdisciplinary

Since da vinci, friction not dependent on object, just friction coefficient

---
3
it's not that simple

coulomb himself found in 1821 that static friction depended on time spent in contact.

-ageing

To explain ageing we need to look at what is going on at a microscopical level.

---
4
Bauberger & Caroli (2009) 

For rough hard solids (which we study) the actual contact area at a microscopic level is much less than
the apparent surface area. The highest peaks at which two solids meet are called 'ASPERITIES'. 

---
5
creep and diffusion

covalent bonds are formed at these asperities, which causes friction.

Ageing can be explained by the fact that the number of covalent bonds increase over time,
as well as the contact area, which in turn increases covalent bonds.

Diffusion is also a factor, as free atoms move about on the surfaces seeking the lowest energy state,
this means atoms settle in crevises where asperities meet, increasing the contact area.

As normal force is increased, naturally contact area is increased aswell, explaining the dependency on 
normal force. 


---
6
rate and state friction

In 1983 Andy Ruina makes an important step in rate and state friction, and writes an equation which does
take into conscideration ageing and other effects which don't correspond to previous ideas of friction.

- theta only dependent on Normal force, slip rate and state itself

- empirical model not fully explaining behaviour

---
8
Fineberg Group

The behaviour of junctions is at the core. Fineberg found rupture fronts

figure b shows a sliding event propogating from the left, all the way to the right.
- full sliding event.
sometimes partial slip events occur.

These show rupture fronts, some of which are fast, and some slow

---
9
How do interacting junctions behave at a microscopical level. Can we use knowledge of interjunctional interactions to understand macroscopic friction?

To study this we need to make a model
---
%% ---------------------------------------------------molecular dynamics----- %%
10
Modeling friction using Molecular dynamics

A numerical method using atom interactions to form materials.
movement of atoms is found using newtons law of motion

Potential is vashista potential, handles three particle distances, and bond angles.
Also handles charges due to multiple atoms SI and C

Integrated using Velocity Verlet. Expanded taylor approximation, but more numerically stable.

%% Mention LAMMPS?%%
---
Choosing a system

In choosing our system there are several aspects we need to conscider.
- realism vs computaional consciderations

We know we want two plates which slide in relation to each other... to have friction
however various factors need to be chosen correctly.

- introduce SiC, and surface energy, lots of diffusion
- perform perliminary simulations to choose system
- asperity shape is based on Sveinsson 2020 paper
- Shape important to energy levels in SiC. Diffusion is more prevalent.
- system is a 4x4 grid

---
->> 10 minutes
top plate variation

-explain load curves
-explain max static
-chess system
-an arbitrarily large system would have no artifacts. when increasing top
plate thickness we expect artifacts to sieze once system is big enough
-one unit cell up adds 72000 atoms. from 735000 to 803000
- bottom plate is (100)
-thinnest top plate is very erratic. all slip at once
- running mean of load curve makes graph smooth

-we choose 2300k as we wish for there to be some diffusion. this has intersting effects.

---
- explain sigmoid fit
- max static friction
- max sigmoid
- rise

---
varying velocity 

- increasing static with higher speeds in accordance with THEMRAL ACTIVATION
- energy level of atom oscilates. every now and then conditions are fulfilled for a bond break
- Trade off raskere hastighet mindre simulering. Dog ønsker så sakte hastighet som mulig.

- we choose 5 m/s
---

varying normal force

- no force -> COHESION (mohr-coulomb)
- no creep effects with no normal force. only wan-der-waals
- less squish with 0

- we choose 0 normal force

---
Bottom plate orientation

- Bottom plate from a different object, hence different orientation
- Doesn't form continous crystal
- continous in x and y direction

---
READY TO SIMULATE
- relax 1 ns, push 1 ns
- periodic boundary conditions
---
2 asperity simulations 1

In order to increase scale we use periodic boundary conditions, this means that asperity configurations have many duplicates.

-We study the 2 asperity systems with the parameters we've chosen earlier
-10 possible configurations
-Assume since we study all possible, this could be a pre-coursor to the eight asperity system with over 700 configurations

-Note norm, we use this later
---
2 asperity simulations 2

-max static affected by noise, use sigmoid fit instead.
- some variation in sigmoid ms
---

8 asperity simulations

---
Machine learning 










