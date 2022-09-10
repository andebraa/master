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

![[temp_coulomb.png|600]]

-> ageing
---



![[baumberger.png]]

Real contact area for rough hard solids is much less than surface area.

The junctions at which surfaces meet are called Asperities.
---
#### creep and diffusion
<split even>
![[ageing_creep.jpeg|400]]
![[ageing_anim.gif|550]]
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

#### Modeling friction using molecular dynamics

![[temp_vashista.png]]
<split even>
![[3c-sic-visualized.png|300]]
![[velocity_verlet.png]]
</split>
---
#### choosing a system
![[choosing_system2.svg]]
Asperity shape based on Sveinsson et. al. (2020)

---
#### Top plate thickness
<split even>
![[load_curves_varying_uc_ms_chess_2300.png|400x400]]
![[max_static_chess_2300_1800.png|500x400]]
</split>
---
#### varying velocity
<split left="1" right="1">
![[vary_vel.png|500x400]]
![[varying_vel_rise_maxstatic.png|500x400]]
</split>

---
#### varying normal force
<split even>
![[vary_normforce.png|500x400]]
![[varying_force_rise_normforce.png|500x400]]
</split>

---
#### 2 asperity system
-periodic boundary conditions causes duplicates
![[2_asp_systems_final.png]]
---

![[production_varying_initnum_temp2300_vel5_force0_asp2_or110_time1400.png|800x800]]
---
![[production_varying_initnum_temp2300_vel5_force0_asp2_or110_time1400_maxstatic_rise_altcolour.png|800x500]]

---
#### The eight asperity case
![[asperity_distance_v_maxstatic.png|600x600]]
---
#### results of selected systems
![[varying_strange.png|600x600]]
---
![[varying_strange_rise_ms.png]]
---
Machine Learning
- Dense Neural Networks
- Convolutional Neural Networks

---
#### Dense Neural Networks (DNN)
![[dnn.png|400x300]]
---
#### Convolutional Neural Networks (CNN)
![[cnn.png|500x300]]
---
#### grid search
![[gridsearch_hyperparameters.png]]
---
#### Machine Learning Results
![[ml_res.png|800x600]]

---
![[ml_res_sigmax.png]]

---

#### Why doesn't configuration matter?
- Two asperity showed promise, but eight saturated the system.
- SiC is a very hard substance. Forces might not propogate through the top plate.
---
#### Diffusion creep
- Asperities don't show stick-slip effects
- High temperature -> High diffusion
- Healing effects

---
#### Summary


---
#### Outlook
