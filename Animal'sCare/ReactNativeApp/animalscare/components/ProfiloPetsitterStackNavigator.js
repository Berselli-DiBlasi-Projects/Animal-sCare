import {createStackNavigator} from 'react-navigation-stack';
import ProfiloPetsitter from '../Pages/ProfiloPetsitter';
import EliminaProfiloConferma from '../Pages/EliminaProfiloConferma';
import ModificaProfiloPetsitter from '../Pages/ModificaProfiloPetsitter';
import AnnunciDiUtente from '../Pages/AnnunciDiUtente';
import RecensioniRicevute from '../Pages/RecensioniRicevute';

const ProfiloPetsitterStackNavigator = createStackNavigator({
    ProfiloPetsitter: {
        screen: ProfiloPetsitter,
        navigationOptions: {
        title: 'Profilo petsitter',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-person" />
          )
        }
    },
    EliminaProfiloConfermaPetsitter: {
        screen: EliminaProfiloConferma,
        navigationOptions: {
        title: 'Elimina profilo conferma'
        }
    },
    ModificaProfiloPetsitter: {
        screen: ModificaProfiloPetsitter,
        navigationOptions: {
            title: 'Modifica profilo'
        }
    },
    AnnunciDiUtentePetsitter: {
        screen: AnnunciDiUtente,
        navigationOptions: {
            title: 'Annunci di utente'
        }
    },
    RecensioniRicevutePetsitter: {
        screen: RecensioniRicevute,
        navigationOptions: {
            title: 'Recensioni ricevute'
        }
    }
}, {headerMode: 'none'});

export default ProfiloPetsitterStackNavigator;