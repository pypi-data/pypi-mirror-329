
Project description

Package created by Kaike Sa Teles Rocha Alves

The evolvingfuzzysystems is a package that contains evolving Fuzzy Systems (eFS) in the context of machine learning models, including the ones developed by Kaike Alves during his Master and PhD. 

    Website: kaikealves.weebly.com
    Documentation: https://doi.org/10.1016/j.asoc.2021.107764
    Email: kaikerochaalves@outlook.com
    https://github.com/kaikerochaalves/evolvingfuzzysystems.git

It provides:

    The package includes the following eFSs: ePL-KRLS-DISCO, ePL+, eMG, ePL, exTS, Simpl_eTS, eTS


Code of Conduct

evolvingfuzzysystems is a library developed by Kaike Alves. Please read the Code of Conduct for guidance.

Call for Contributions

The project welcomes your expertise and enthusiasm!

Small improvements or fixes are always appreciated. If you are considering larger contributions to the source code, please contact by email first.

To install the library use the command: 

    pip install evolvingfuzzysystems

To import the ePL-KRLS-DISCO, simply type the command:

    from evolvingfuzzysystems.eFS import ePL_KRLS_DISCO

To import the ePL+, simply type:

    from evolvingfuzzysystems.eFS import ePL_plus

To import the eMG, type:

    from evolvingfuzzysystems.eFS import eMG

To import the ePL, type:

    from evolvingfuzzysystems.eFS import ePL

To import the exTS, type:

    from evolvingfuzzysystems.eFS import exTS

To import the Simpl_eTS, type:

    from evolvingfuzzysystems.eFS import Simpl_eTS

To import the eTS, type:

    from evolvingfuzzysystems.eFS import eTS

You can learn more about the ePL-KRLS-DISCO and eFSs in the paper: https://doi.org/10.1016/j.asoc.2021.107764.


Usage examples

Once you imported the libraries, you can use functions fit, evolve and predict. For example:

    from evolvingfuzzysystems.eFS import ePL_KRLS_DISCO
    model = ePL_KRLS_DISCO()
    model.fit(X_train, y_train)
    model.evolve(X_val, y_val)
    y_pred = model.predict(y_test)

If you want to see how many rules was generated, you can type:

    model.n_rules()

You can see the rules graphically by typing:

    model.plot_rules()

If you want to see all Gaussian fuzzy sets, type:

    model.plot_gaussians()

To see the evolution of the rules along with the training, type:

    model.plot_rules_evolution()

For the eMG model, as it uses covariance matrix to model the distribution of the input vector, if you want to visualize the covariance between two attributes, type:

    model.plot_2d_projections()

These last four function that plots graphics accepts extra arguments:

    grid (boolean): if you want the graphic with grid
    save (boolean): if you want to save the graphic
    format_save (default='eps'): the format you want to save the graphic.
    dpi (integer, default=1200): the resolution to save the graphic

If you think you can contribute to this project regarding the code, speed, etc., please, feel free to contact me and to do so.
