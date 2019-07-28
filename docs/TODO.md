## TODO

* Testing
    * Check invalid inputs --> e.g. [1, [2, 3]]
    * Add test cases for matrices >2D

* Features
    * Return name of layer
        * >>> Atmosphere(0).layer_name --> 'Troposphere'
        * Add test cases!
    * Converters (--> separate class?)
        * bar to MPa

* Change
    * Rename 't2T' to 'celsius2kelvin' and vice versa

* Optimising
    * Try to avoid multiple calls of '_get_layer_params'
