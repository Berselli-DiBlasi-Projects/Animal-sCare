import {createStackNavigator} from 'react-navigation-stack';
import Classifica from '../Pages/Classifica';
import ProfiloUtenteClassificaSN from './ProfiloUtenteStackNavigator';

const ClassificaStackNavigator = createStackNavigator({
    Classifica: {
        screen: Classifica,
        navigationOptions: {
        title: 'Classifica',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-search" />
          )
        }
    },
    ProfiloUtenteClassificaSN: {
        screen: ProfiloUtenteClassificaSN,
        navigationOptions: {
        title: 'Profilo utente'
        }
    }

}, {headerMode: 'none'});

export default ClassificaStackNavigator;