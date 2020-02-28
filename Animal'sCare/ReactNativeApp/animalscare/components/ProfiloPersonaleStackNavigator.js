import React, { Component, createContext } from 'react';
import {createStackNavigator} from 'react-navigation-stack';
import ProfiloPersonale from '../Pages/ProfiloPersonale';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';
import ModificaProfilo from '../Pages/ModificaProfilo';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';


const ProfiloPersonaleStackNavigator = createStackNavigator({
    ProfiloPersonale: {
        screen: ProfiloPersonale,
        navigationOptions: {
            title: 'Profilo',
            drawerIcon: ({ tintColor }) => (
                <Icon name = "md-person" />
            )
        }
    },
    EliminaProfiloConferma: {
        screen: EliminaProfiloConferma,
        navigationOptions: {
            title: 'Elimina profilo conferma'
        }
    },
    ModificaProfilo: {
        screen: ModificaProfilo,
        navigationOptions: {
            title: 'Modifica profilo'
        }
    },
    AnnunciDiUtente: {
        screen: AnnunciDiUtente,
        navigationOptions: {
            title: 'Annunci di utente'
        }
    },
    RecensioniRicevute: {
        screen: RecensioniRicevute,
        navigationOptions: {
            title: 'Recensioni ricevute'
        }
    }
}, {headerMode: 'none'});

export default ProfiloPersonaleStackNavigator;