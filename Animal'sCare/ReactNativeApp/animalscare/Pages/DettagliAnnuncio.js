import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, ActivityIndicator } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import annuncio_default from '../assets/annuncio_default.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import AutoHeightImage from 'react-native-auto-height-image';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

let id_annuncio;

class DettagliAnnuncio extends Component {

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true,
            id_annuncio: this.props.navigation.state.params.id_annuncio
        }
    }

    componentDidMount() {
        this.fetchDettagliAnnuncio();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.fetchDettagliAnnuncio();
          }
        );
    }

    componentWillUnmount() {
    this.willFocusSubscription.remove();
    }

    fetchDettagliAnnuncio() {
        return fetch('http://2.224.160.133.xip.io/api/annunci/' + this.props.navigation.state.params.id_annuncio + '/dettagli/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {
        
        this.setState({
            isLoading: false,
            id_annuncio: this.props.navigation.state.params.id_annuncio,
            dataSource: responseJson,
        }, function(){

        });

        })
        .catch((error) =>{
        this.fetchDettagliAnnuncio();
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

        n_servizi = 0;
        servizi = "";

        if(data.passeggiate) {
            servizi += "Passeggiate";
            n_servizi += 1;
        }
        if(data.pulizia_gabbia) {
            if (n_servizi > 0) {
                servizi += " , ";
            }
            servizi += "Pulizia gabbia";
            n_servizi += 1;
        }
        if(data.ore_compagnia) {
            if (n_servizi > 0) {
                servizi += " , ";
            }
            servizi += "Ore di compagnia";
            n_servizi += 1;
        }
        if(data.cibo) {
            if (n_servizi > 0) {
                servizi += " , ";
            }
            servizi += "Dare da mangiare";
            n_servizi += 1;
        }
        if(data.accompagna_dal_vet) {
            if (n_servizi > 0) {
                servizi += " , ";
            }
            servizi += "Accompagna dal veterinario";
            n_servizi += 1;
        }

        return (
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        {data.annuncio.titolo}
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>
                
                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        
                        <AutoHeightImage width={width - width / 30} 
                            source={ data.annuncio.logo_annuncio ? { uri: data.annuncio.logo_annuncio } : annuncio_default } />
                                    
                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Sottotitolo: </Text>
                                    <Text style={styles.textData}>{data.annuncio.sottotitolo}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Descrizione: </Text>
                                    <Text style={styles.textData}>{data.annuncio.descrizione}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Pet coins: </Text>
                                    <Text style={styles.textData}>{data.annuncio.pet_coins}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Pubblicato da: </Text>
                                    <Text style={styles.textData}>{data.annuncio.user.username}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Pet: </Text>
                                    <Text style={styles.textData}>{data.annuncio.pet}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Data inizio: </Text>
                                    <Text style={styles.textData}>{data.annuncio.data_inizio}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Data fine: </Text>
                                    <Text style={styles.textData}>{data.annuncio.data_fine}</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Posizione: </Text>
                                    <Text style={styles.textData}>INSERIRE MAPPA</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Servizi richiesti: </Text>
                                    <Text style={styles.textData}>{servizi}</Text>
                                </View>

                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Accetta annuncio" onPress={() => this.props.navigation.navigate('AccettaAnnuncioConferma', {id_annuncio: this.state.id_annuncio})}/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Modifica annuncio" onPress={() => this.props.navigation.navigate('ModificaAnnuncio')}/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Elimina annuncio" color='red' onPress={() => this.props.navigation.navigate('EliminaAnnuncioConferma', {id_annuncio: this.state.id_annuncio})} />
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
        paddingTop: 20
    },
    buttonview: {
        width: 110,
        paddingRight: 5,
        paddingLeft: 5
    },
    inputContainer: {
        minWidth: '96%',
        flexDirection: 'row'
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

export default DettagliAnnuncio;