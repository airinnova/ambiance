## TODO

* Handle *matrices* as input

* Better treatment of layer specific data
    * Make pseudo layers?

* Testing
    * Check invalid inputs --> e.g. [1, [2, 3]]
    * Add test cases for boundaries layers

* Features
    * Return name of layer
        * >>> Atmosphere(0).layer_name --> 'Troposphere'
    * Converters (--> separate class?)
        * bar to MPa
