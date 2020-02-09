import {createStackNavigator} from 'react-navigation-stack';
import ProfiloNormale from '../Pages/ProfiloNormale';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';
import ModificaProfiloNormale from '../Pages/ModificaProfiloNormale';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';

const ProfiloNormaleStackNavigator = createStackNavigator({
    ProfiloNormale: {
        screen: ProfiloNormale,
        navigationOptions: {
        title: 'Profilo normale',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-person" />
          )
        }
    },
    EliminaProfiloConfermaNormale: {
        screen: EliminaProfiloConferma,
        navigationOptions: {
        title: 'Elimina profilo conferma'
        }
    },
    ModificaProfiloNormale: {
        screen: ModificaProfiloNormale,
        navigationOptions: {
            title: 'Modifica profilo'
        }
    },
    AnnunciDiUtenteNormale: {
        screen: AnnunciDiUtente,
        navigationOptions: {
            title: 'Annunci di utente'
        }
    },
    RecensioniRicevuteNormale: {
        screen: RecensioniRicevute,
        navigationOptions: {
            title: 'Recensioni ricevute'
        }
    }
}, {headerMode: 'none'});

export default ProfiloNormaleStackNavigator;