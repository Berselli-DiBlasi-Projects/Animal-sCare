import {createStackNavigator} from 'react-navigation-stack';
import Registrazione from '../Pages/Registrazione';
import RegistrazioneNormale from '../Pages/RegistrazioneNormale';
import RegistrazionePetsitter from '../Pages/RegistrazionePetsitter';

const RegistrazioneStackNavigator = createStackNavigator({
    Registrazione: {
        screen: Registrazione,
          navigationOptions: {
          title: 'Registrazione'
          }
    },
    RegistrazioneNormale: {
        screen: RegistrazioneNormale,
        navigationOptions: {
            title: 'Registrazione normale'
        }
    },
    RegistrazionePetsitter: {
        screen: RegistrazionePetsitter,
        navigationOptions: {
            title: 'Registrazione petsitter'
        }
    }
}, {headerMode: 'none'});

export default RegistrazioneStackNavigator;