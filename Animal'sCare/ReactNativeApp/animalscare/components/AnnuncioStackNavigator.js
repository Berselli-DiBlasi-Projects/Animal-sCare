import {createStackNavigator} from 'react-navigation-stack';
import DettagliAnnuncio from '../Pages/DettagliAnnuncio';
import AccettaAnnuncioConferma from '../Pages/AccettaAnnuncioConferma';
import EliminaAnnuncioConferma from '../Pages/EliminaAnnuncioConferma';
import ModificaAnnuncio from '../Pages/ModificaAnnuncio';

const AnnuncioStackNavigator = createStackNavigator({
    DettagliAnnuncio: {
        screen: DettagliAnnuncio,
        navigationOptions: {
        title: 'Dettagli annuncio'
        }
    },
    AccettaAnnuncioConferma: {
        screen: AccettaAnnuncioConferma,
        navigationOptions: {
        title: 'Accetta annuncio conferma'
        }
    },
    EliminaAnnuncioConferma: {
        screen: EliminaAnnuncioConferma,
        navigationOptions: {
        title: 'Elimina annuncio conferma'
        }
    },
    ModificaAnnuncio: {
        screen: ModificaAnnuncio,
        navigationOptions: {
        title: 'Modifica annuncio'
        }
    }
}, {headerMode: 'none'});

export default AnnuncioStackNavigator;