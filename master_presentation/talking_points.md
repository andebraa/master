0
Predicting static friction in a molecular dynamic system using machine learning
-> interjunctional asperities

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

Since da vinci, friction not dependent on object, just friction coefficient

---
3
it's not that simple

coulomb himself found in 1821 that static friction depended on time spent in contact.

-ageing

Also the fact that transition from static to dynamic is not infinitely sharp.
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

In order to explore this we made a system of two plates with a 4x4 grid with two and eight asperities inbetween.

---
%% ---------------------------------------------------molecular dynamics----- %%
10
Modeling friction using Molecular dynamics

A numerical method using atom interactions to form materials.
movement of atoms is found using newtons law of motion

Potential is vashista potential, handles three particle distances, and bond angles.
Also handles charges due to multiple atoms SI and C

Integrated using Velocity Verlet. Expanded taylor approximation, but more numerically stable.

---
Choosing a system

-junction between realism and computational consciderations




