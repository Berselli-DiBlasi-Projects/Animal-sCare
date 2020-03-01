import React, { Component, createContext } from 'react';
import {createStackNavigator} from 'react-navigation-stack';
import ProfiloUtente from '../Pages/ProfiloUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';
import ModificaProfilo from '../Pages/ModificaProfilo';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';


const ProfiloUtenteStackNavigator = createStackNavigator({
    ProfiloUtente: {
        screen: ProfiloUtente,
        navigationOptions: {
            title: 'Profilo'
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

export default ProfiloUtenteStackNavigator;