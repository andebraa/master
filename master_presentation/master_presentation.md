---
theme: solarized
---

## Predicting static friction in a molecular dynamic system using machine learning

#### _Interjunctional Asperity Relations_

---
![[initial_system_2asp_initnum3_render.png]]
---
### presentation contents
- Introduction to friction
	- Why is it important to study
- Modeling friction
	- Molecular Dynamics
- Choosing and simulating a system
- Analysis 
	- Machine learning
- Results and discussion
---
### Friction
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
### It's not that simple

![[temp_coulomb.png|600]]

-> Real contact area and ageing
---



![[baumberger.png]]

Real contact area for rough hard solids is much less than surface area.

The junctions at which surfaces meet are called Asperities.
---
### Creep and diffusion
<split even>
![[ageing_creep.jpeg|400]]
![[ageing_anim.gif|550]]
</split>
---

### Rate and state
![[ruina_experiment.png|300x200]]

Ruina et. al. (1983)
$$
\begin{equation}
    \mu = \mu_0 a \ln \left( 1 + \frac{1}{v_0}\right) + b \ln \left( \frac{v_0 \theta(t)}{d_0} \right).
\end{equation}
$$
Dependent on split rate and state variables $\theta(t)$. 
- Empirical

---
### Fineberg group

"Static Friction Coefficient is Not a Material Constant" (2011)
![[finebert_experiment.png]]

---
How do interacting junctions behave at a microscopical level. Can we use knowledge of interjunctional interactions to understand macroscopic friction?
![[initial_system_2asp_initnum3_render.png]]

---

### Modeling friction using molecular dynamics

![[temp_vashista.png]]
<split even>
![[3c-sic-visualized.png|300]]
![[velocity_verlet.png]]
</split>
---
### Choosing a system
![[choosing_system2.svg]]
Asperity shape based on Sveinsson et. al. (2020)
---
![[temp_chess_system_viz.png]]
---
### Top plate thickness
<split even>
![[load_curves_varying_uc_ms_chess_2300.png|400x400]]
![[max_static_chess_2300_1800.png|500x400]]
</split>
---
![[temp_zoomed_loadcurve.png]]
---
### Varying velocity
<split left="1" right="1">
![[vary_vel.png|500x400]]
![[varying_vel_rise_maxstatic.png|500x400]]
</split>

\begin{equation}
    F \propto c - T^{2/3} |\ln v/T|^{2/3}.
\end{equation}


---
### Varying normal force
<split even>
![[vary_normforce.png|500x400]]
![[varying_force_rise_normforce.png|500x400]]
</split>
\begin{equation}
    \mu_s = F_n \tan(\phi) + c,
\end{equation}
Mohr-Coulomb (1777)
---
### Bottom plate orientation
![[identify_diamond_comb.png]]
---
### Ready to simulate
![[visualized_system.gif]]

---
### 2 asperity system
- Periodic boundary conditions causes duplicates
![[2_asp_systems_final.png]]
- Asperity-asperity norm
---

![[production_varying_initnum_temp2300_vel5_force0_asp2_or110_time1400.png|800x800]]

---
![[production_varying_initnum_temp2300_vel5_force0_asp2_or110_time1400_maxstatic_rise_altcolour.png|800x500]]

---
### The eight asperity case
![[asperity_distance_v_maxstatic.png|600x600]]
---
### Simulating selected systems
![[strange_system_visualized.svg]]
---
#### Results of selected systems

![[varying_strange.png|600x600]]
---
![[varying_strange_rise_ms.png]]
---
Machine Learning
- Dense Neural Networks
- Convolutional Neural Networks

---
### Dense Neural Networks (DNN)
![[dnn.png|400x300]]
---
### Convolutional Neural Networks (CNN)
![[cnn.png|500x300]]
---

### $R^2$ and MSE

$
R^2 = 1 - \frac{\sum_i (y_i - y_i^*)^2}{\sum_i (y_i - \overline{y})^2},
$
$
MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$


---
![[ml_data_distribution.png]]
---
#### Grid search

![[gridsearch_hyperparameters.png]]
---
### Machine Learning Results
![[ml_res_sigmax.png]]

---

### Why doesn't configuration matter?
- Two asperity showed promise, but eight saturated the system.
- SiC is a very hard substance. Forces might not propogate through the top plate.
---
### Diffusion creep
- Asperities don't show stick-slip effects
- High temperature -> High diffusion
- Healing effects
---

### Thesis summary
- Systems and simulations
	- Made a system for simulating friction with a flexible configuration
	- Limited scope to asperity configuration
	- Identified unique systems based on periodic boundaries
	- Simulated 320 systems
---

- Methods for analyzing the system
	- Norm of asperity distances
	- Maximum static friction
	- Sigmoid fit
---
- Machine learning
	- CNN and DNN applied to confirm little asperity configuration dependency
	- Application of random dataset for baseline
---
### Result summary
- Effects such as cohesion, thermal actiavtion and linear dependence on normal force confirmed
- Static friction in our system is independent from asperity configuration
- Effects of diffusion creep altered the system behaviour

---
### outlook
- Numerous variations of the system can be made
- Lower temperature for less diffusion and healing effects
- Increase system if computationally feasible or decrease number of asperities
- Calculate real contact area of asperities
- Observe each asperity individually for rupture behaviour
---
---
![[ml_res.png|800x600]]