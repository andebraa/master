---
theme: solarized
---

## Predicting static friction in a molecular dynamic system using machine learning

#### _Interjunctional Asperity Relations_

---

### presentation contents
- introduction to friction
- Molecular Dynamcs
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
#### rate and state
<split even>
![[temp_coulomb.png|300x200]]
![[ruina_experiment.png|300x200]]
</split>

- ruina et. al. (1983)
$$
\begin{equation}
    \mu = \mu_0 a \ln \left( 1 + \frac{1}{v_0}\right) + b \ln \left( \frac{v_0 \theta(t)}{d_0} \right).
\end{equation}
$$
---
#### Ageing and Real Surface Areas
<split even>
![[temp_surfaces.png]]
</split>
![[li_etal.png|500x400]]

---
Fineberg group

"Static Friction Coefficient is Not a Material Constant" (2011)
![[fig/temp_rupture_front.png|500]]

--> there is a lot more going on

---
### how do we model friction?
<split even>
![[spring_model.png|300x500]] 

test
</split> 
---
### Molecular dynamics

- Potentials and forces
- Numerical methods

---
#### lennard-jones potential
$$
\begin{equation}
    V(r_{i,j}) = 4 \epsilon \left[(\frac{\sigma}{r_{i.j}})^{12} - (\frac{\sigma}{r_{i,j}})^6\right]
\end{equation}
$$
![[LJ_WW_Pauli.png|450x300]]
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
