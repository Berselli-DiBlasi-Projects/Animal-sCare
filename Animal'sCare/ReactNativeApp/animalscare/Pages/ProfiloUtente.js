import React, { Component, useContext } from 'react';
import { View, Text, StyleSheet, Button, Image, ActivityIndicator } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import user_default from '../assets/user_default.jpg';
import pet_default from '../assets/pet_default.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import AutoHeightImage from 'react-native-auto-height-image';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class ProfiloUtente extends Component {

    user_id = -1;

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true
        }
    }
    
    componentDidMount() {
        this.user_id = this.props.navigation.state.params.user_id;
        this.fetchProfilo();
        
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true
            });
            
            this.user_id = this.props.navigation.state.params.user_id;
            this.fetchProfilo();
          }
        );
    }

    componentWillUnmount() {
    this.willFocusSubscription.remove();
    }

    fetchProfilo() {
        return fetch('http://2.224.160.133.xip.io/api/utenti/profilo/' + this.user_id + '/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {
        
        this.setState({
            isLoading: false,
            dataSource: responseJson
        }, function(){

        });

        })
        .catch((error) =>{
        this.fetchProfilo();
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

        data = this.state.dataSource;

        let label_annunci_di = 'Annunci di ' + data.user.username;

        if (data.pet_sitter == false) { // Utente normale

            return (
                <View style={styles.screen}>
                    
                    <CustomHeader parent={this.props} />
                    
                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Profilo di {data.user.username}
                        </Text>
                        <View style={styles.rightcontainer}></View>
                    </View>
                    
                    <ScrollView showsVerticalScrollIndicator={false}>
                        <View style={{alignItems: 'center'}}>
                            <AutoHeightImage width={width - width / 30} 
                                source={ data.foto_profilo ? { uri: data.foto_profilo } : user_default } />
    
                            <Card style={styles.inputContainer}>
                                <View style={styles.data}>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Utente normale</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Nome: </Text>
                                        <Text style={styles.textData}>{data.user.first_name}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Cognome: </Text>
                                        <Text style={styles.textData}>{data.user.last_name}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Email: </Text>
                                        <Text style={styles.textData}>{data.user.email}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Indirizzo: </Text>
                                        <Text style={styles.textData}>{data.indirizzo}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Città: </Text>
                                        <Text style={styles.textData}>{data.citta}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Provincia: </Text>
                                        <Text style={styles.textData}>{data.provincia}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Regione: </Text>
                                        <Text style={styles.textData}>{data.regione}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Posizione: </Text>
                                        <Text style={styles.textData}>INSERIRE MAPPA</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Telefono: </Text>
                                        <Text style={styles.textData}>{data.telefono}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Voti: </Text>
                                        <Text style={styles.textData}>{data.media_voti}/5</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Recensioni: </Text>
                                        <Text style={styles.textData}>{data.numero_recensioni} recensione</Text>
                                    </View>
                                </View>
                            </Card>
    
                            <AutoHeightImage width={width - width / 30} 
                                source={ data.foto_pet ? { uri: data.foto_pet } : pet_default } />
    
                            <Card style={styles.inputContainer}>
                                <View style={styles.data}>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Nome pet: </Text>
                                        <Text style={styles.textData}>{data.nome_pet}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Razza: </Text>
                                        <Text style={styles.textData}>{data.razza}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Età pet: </Text>
                                        <Text style={styles.textData}>{data.eta}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Caratteristiche: </Text>
                                        <Text style={styles.textData}>{data.caratteristiche}</Text>
                                    </View>
    
                                    <View style={styles.controlli}>
                                        <View style={styles.buttonview}>
                                            <Button title={label_annunci_di} onPress={() => this.props.navigation.navigate('AnnunciDiUtente', {user_id: data.user.id, username: data.user.username})} />
                                        </View>
                                        <View style={styles.buttonview}>
                                            <Button title="Recensioni ricevute" onPress={() => this.props.navigation.navigate('RecensioniRicevute', {username: data.user.username})}/>
                                        </View>
                                    </View>
                                </View>
                            </Card>    
                        </View>
                    </ScrollView>
                </View>
            );

        } else { // Utente petsitter

            return (
                <View style={styles.screen}>
                    
                    <CustomHeader parent={this.props} />
                    
                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Profilo di {data.user.username}
                        </Text>
                        <View style={styles.rightcontainer}></View>
                    </View>
                    
                    <ScrollView showsVerticalScrollIndicator={false}>
                        <View style={{alignItems: 'center'}}>
                            <AutoHeightImage width={width - width / 30}
                                source={ data.foto_profilo ? { uri: data.foto_profilo } : user_default } />
    
                            <Card style={styles.inputContainer}>
                                <View style={styles.data}>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Utente petsitter</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Nome: </Text>
                                        <Text style={styles.textData}>{data.user.first_name}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Cognome: </Text>
                                        <Text style={styles.textData}>{data.user.last_name}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Email: </Text>
                                        <Text style={styles.textData}>{data.user.email}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Indirizzo: </Text>
                                        <Text style={styles.textData}>{data.indirizzo}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Città: </Text>
                                        <Text style={styles.textData}>{data.citta}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Provincia: </Text>
                                        <Text style={styles.textData}>{data.provincia}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Regione: </Text>
                                        <Text style={styles.textData}>{data.regione}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Posizione: </Text>
                                        <Text style={styles.textData}>INSERIRE MAPPA</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Telefono: </Text>
                                        <Text style={styles.textData}>{data.telefono}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Descrizione: </Text>
                                        <Text style={styles.textData}>{data.descrizione}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Hobby: </Text>
                                        <Text style={styles.textData}>{data.hobby}</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Voti: </Text>
                                        <Text style={styles.textData}>{data.media_voti}/5</Text>
                                    </View>
                                    <View style={styles.entry}>
                                        <Text style={styles.textTitle}>Recensioni: </Text>
                                        <Text style={styles.textData}>{data.numero_recensioni} recensioni</Text>
                                    </View>
    
                                    <View style={styles.controlli}>
                                        <View style={styles.buttonview}>
                                            <Button title={label_annunci_di} onPress={() => this.props.navigation.navigate('AnnunciDiUtente', {user_id: data.user.id, username: data.user.username})}/>
                                        </View>
                                        <View style={styles.buttonview}>
                                            <Button title="Recensioni ricevute" onPress={() => this.props.navigation.navigate('RecensioniRicevute', {username: data.user.username})}/>
                                        </View>
                                    </View>
                                </View>
                            </Card>
                        </View>
                    </ScrollView>
                </View>
            );
        }
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1
    },
    title: {
        fontSize: 20,
        marginVertical: 10,
        textAlign: 'center'
    },
    data: {
        paddingTop: 20,
        paddingLeft: 10
    },
    entry: {
        paddingTop: 10,
        flexDirection: 'row'
    },
    textTitle: {
        fontWeight: 'bold'
    },
    textData: {
        width: width - width / 3
    },
    controlli: {
        flexDirection: 'row',
        justifyContent: 'center',
        paddingTop: 20
    },
    buttonview: {
        width: width - width / 1.45,
        paddingRight: width - width / 1.03
    },
    inputContainer: {
        minWidth: '100%',
        flexDirection: 'row',
        alignContent: 'center'
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
    }
});

export default ProfiloUtente;