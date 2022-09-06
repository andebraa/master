:---
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
- Da Vinci, Amontons (1699) , Coulomb et. al (1821). 
$$
\begin{aligned}
f \leq& \mu_s F_n &, v = 0\\
f =& -sign(v) \mu_d F_N &, v \neq 0.
\end{aligned}
$$

---
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
![[temp_coulomb.png|300x200]]
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
![[spring_model.png]] 

test
</split> 
---
### Molecular dynamics

- Potentials and forces
- Numerical methods

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
