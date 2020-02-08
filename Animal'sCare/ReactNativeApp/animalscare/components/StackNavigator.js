import {createStackNavigator} from 'react-navigation-stack';
import DettagliAnnuncio from '../Pages/DettagliAnnuncio';
import AccettaAnnuncioConferma from '../Pages/AccettaAnnuncioConferma';
import EliminaAnnuncioConferma from '../Pages/EliminaAnnuncioConferma';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';

const CustomStackNavigator = createStackNavigator({
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
    EliminaProfiloConferma: {
        screen: EliminaProfiloConferma,
        navigationOptions: {
        title: 'Elimina profilo conferma'
        }
    }
}, {headerMode: 'none'});

export default CustomStackNavigator;