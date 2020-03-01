import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions, ActivityIndicator, FlatList, YellowBox } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import profilo_default from '../assets/user_default.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';
import { IconButton, ThemeProvider } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class Classifica extends Component {

    tipo_utente = "*"; // *, petsitter, normale
    criterio = "voti"; // voti, recensioni

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true,
            show_pickers: true
        }
    }

    ShowHidePickers = () => {
        if (this.state.show_pickers == true) {
          this.setState({ show_pickers: false });
        } else {
          this.setState({ show_pickers: true });
        }
    };
    
    componentDidMount() {
        this.fetchUtenti();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.fetchUtenti();
          }
        );
    }

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    }

    fetchUtenti(){
    return fetch('http://2.224.160.133.xip.io/api/utenti/classifica/' + this.tipo_utente
         + '/' + this.criterio + '/?format=json')

        .then((response) => response.json())
        .then((responseJson) => {

        this.setState({
            isLoading: false,
            dataSource: responseJson,
        }, function(){

        });
        })
        .catch((error) =>{
            this.fetchUtenti();
        });
    }

    render() {

        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        YellowBox.ignoreWarnings([
            'VirtualizedLists should never be nested',
        ])
        
        return (
            
            <View style={styles.screen}>

                <View style={{alignSelf: 'flex-start', width: '100%', alignItems: 'center'}}>
                    <CustomHeader parent={this.props} />

                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Classifica
                        </Text>
                        <View style={styles.rightcontainer}>
                            <IconButton icon="filter" style={{paddingRight: 10}} onPress={this.ShowHidePickers} />
                        </View>
                    </View>
                    
                    {this.state.show_pickers ? (
                        <View style={styles.pickers}>
                            <Picker
                                style={styles.picker} itemStyle={styles.pickerItem}
                                selectedValue={this.tipo_utente}
                                onValueChange={(itemValue) => { this.tipo_utente = itemValue;
                                    this.fetchUtenti();}}
                                >
                                <Picker.Item label="Classifica generale" value="*" />
                                <Picker.Item label="Classifica dei petsitter" value="petsitter" />
                                <Picker.Item label="Classifica degli utenti normali" value="normale" />
                            </Picker>

                            <View style={{paddingBottom: 5}}></View>
                        
                            <Picker
                                style={styles.picker} itemStyle={styles.pickerItem}
                                selectedValue={this.criterio}
                                onValueChange={(itemValue) => {this.criterio = itemValue;
                                    this.fetchUtenti();}}
                                >
                                <Picker.Item label="Ordina per voto" value="voti" />
                                <Picker.Item label="Ordina per numero di recensioni ricevute" value="recensioni" />
                            </Picker>

                            <View style={{paddingBottom: 2}}></View>
                        </View>
                    ) : null}
                </View>
                <View style={styles.flatlistview}>
                    <FlatList
                        style={{flex: 1}}
                        data={this.state.dataSource}
                        renderItem={({item, index}) => 
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloUtenteClassificaSN', {user_id: item.user.id})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={ item.foto_profilo ? { uri: item.foto_profilo } : profilo_default }
                                     style={styles.profileLogo}  />
                                </View>
                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>{item.user.first_name} {item.user.last_name}</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>{item.pet_sitter == true ? 'Petsitter' : 'Utente normale'},
                                         {item.indirizzo}, {item.citta}</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>{item.media_voti}/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>{item.numero_recensioni}</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
                        }
                        keyExtractor={(item, index) => index.toString()}
                    />
                </View>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        alignItems: 'center'
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainer: {
        flex: 1,
        minWidth: '96%',
        flexDirection: 'row'
    },
    data: {
        flex: 1
    },
    image: {
        paddingRight: 10
    },
    textInline: {
        flexDirection: 'row'
    },
    touchableopacity: {
        flex: 1,
        alignItems: 'center'
    },
    picker: {
        width: '100%',
        height: 40,
        backgroundColor: '#e7e7e7',
        borderColor: 'black',
        borderWidth: 3
    },
    pickerItem: {
        color: 'white'
    },
    contentbar: {
        height: 50,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    leftcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-start'
    },
    rightcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center'
    },
    pickers: {
        height: 87,
        width: '90%',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    flatlistview: {
        flex: 1,
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    profileLogo: {
        width: 80,
        height: 80
    },
    profileName: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    profileData: {
        width: width - width / 2.6
    }
});

export default Classifica;