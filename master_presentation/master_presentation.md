---
theme: solarized
---

## Predicting static friction in a molecular dynamic system using machine learning

#### _Interjunctional Asperity Relations_

---

### presentation contents
- introduction to friction
	- why is it important to study
- modeling friction
	- Molecular Dynamcs
- choosing and simulating a system
- analysis 
	- Machine learning
- Results and discussion

---
#### Friction
_Forces which resist relative motion_
![[davinchi_experiemnt.png.svg]]
- Da Vinci, Amontons (1699) , Coulomb et. al (1821). 
$$
\begin{aligned}
f \leq& \mu_s F_n &, v = 0\\
f =& -sign(v) \mu_d F_N &, v \neq 0.
\end{aligned}
$$

---
#### it's not that simple

![[temp_coulomb.png|400]]

-> ageing
---



![[baumberger.png]]
%% ###### Baumberger & Caroli (2009) %%

Real contact area for rough hard solids is much less than surface area.

The junctions at which surfaces meet are called Asperities.
---
#### creep and diffusion
<split even>
![[ageing_creep.jpeg|400]]
![[ageing_anim.gif]]
</split>
---

#### rate and state
![[ruina_experiment.png|300x200]]

ruina et. al. (1983)
$$
\begin{equation}
    \mu = \mu_0 a \ln \left( 1 + \frac{1}{v_0}\right) + b \ln \left( \frac{v_0 \theta(t)}{d_0} \right).
\end{equation}
$$
dependent on split rate and state variables $\theta(t)$

---
Fineberg group

"Static Friction Coefficient is Not a Material Constant" (2011)
![[finebert_experiment.png]]

---
How do interacting junctions behave at a microscopical level. Can we use knowledge of interjunctional interactions to understand macroscopic friction?

![[initial_system_2asp_initnum3_render.png]]
---
%%Drop this slide? %%
%%
### how do we model friction?
![[spring_model.png|300x500]] 

$$
\begin{equation}
	i \hbar \frac{\partial \psi(\vec{r},t)}{\partial t} = \frac{\hbar^2}{2m} \nabla^2 \psi(\vec{r}, t) + V\psi(\vec{r}, t)
\end{equation}
$$ 
---
%%
#### Modeling friction using molecular dynamics
<split left="2" right="1">
![[temp_vashista.png]]
![[3c-sic-visualized.png]]
</split>
![[velocity_verlet.png|300]]

---
#### choosing a system
![[choosing_system2.svg]]
Asperity shape based on Sveinsson et. al. (2020)

---


Machine Learning
- DNN
- CNN

---
Models and Methods
- Potentials and forces
- Computational consciderations
- Choosing a system

---
