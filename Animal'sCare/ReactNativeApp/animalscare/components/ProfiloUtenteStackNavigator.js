import React, { Component, createContext } from 'react';
import {createStackNavigator} from 'react-navigation-stack';
import ProfiloUtente from '../Pages/ProfiloUtente';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';


const ProfiloUtenteStackNavigator = createStackNavigator({
    ProfiloUtente: {
        screen: ProfiloUtente,
        navigationOptions: {
            title: 'Profilo'
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

export default ProfiloUtenteStackNavigator;