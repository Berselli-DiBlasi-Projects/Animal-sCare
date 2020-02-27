import {createStackNavigator} from 'react-navigation-stack';
import Profilo from '../Pages/Profilo';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';
import ModificaProfilo from '../Pages/ModificaProfilo';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';

const ProfiloStackNavigator = createStackNavigator({
    Profilo: {
        screen: Profilo,
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

export default ProfiloStackNavigator;