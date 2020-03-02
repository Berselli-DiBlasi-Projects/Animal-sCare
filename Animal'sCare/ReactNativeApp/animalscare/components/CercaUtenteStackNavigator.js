import {createStackNavigator} from 'react-navigation-stack';
import CercaUtente from '../Pages/CercaUtente';
import ProfiloUtenteCercaUtenteSN from './ProfiloUtenteStackNavigator';

const CercaUtenteStackNavigator = createStackNavigator({
    CercaUtente: {
        screen: CercaUtente,
        navigationOptions: {
        title: 'Cerca utente',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-search" />
          )
        }
    },
    ProfiloUtenteCercaUtenteSN: {
        screen: ProfiloUtenteCercaUtenteSN,
        navigationOptions: {
        title: 'Profilo utente'
        }
    }

}, {headerMode: 'none'});

export default CercaUtenteStackNavigator;