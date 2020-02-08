import React, { Component, useContext } from 'react';
import { View, Text, StyleSheet, Button, Image } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card'
import profile_image from '../assets/profile_img2.png';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import AutoHeightImage from 'react-native-auto-height-image';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

let id_utente;

class ProfiloPetsitter extends Component {

    render() {
        id_utente = 2;
        
        return (
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.navigate('ListaAnnunci')} />
                    </View>
                    <Text style={styles.title}>
                        Profilo con id {id_utente}
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>
                
                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        <AutoHeightImage width={width - width / 30} source={profile_image} />

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Nome: </Text>
                                    <Text style={styles.textData}>Laura</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Cognome: </Text>
                                    <Text style={styles.textData}>Verdi</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Email: </Text>
                                    <Text style={styles.textData}>laura@gmail.com</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Indirizzo: </Text>
                                    <Text style={styles.textData}>Via Corassori 5</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Città: </Text>
                                    <Text style={styles.textData}>Formigine</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Provincia: </Text>
                                    <Text style={styles.textData}>MO</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Regione: </Text>
                                    <Text style={styles.textData}>Emilia Romagna</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Posizione: </Text>
                                    <Text style={styles.textData}>INSERIRE MAPPA</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Telefono: </Text>
                                    <Text style={styles.textData}>3391620711</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Descrizione: </Text>
                                    <Text style={styles.textData}>Amo gli animali</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Hobby: </Text>
                                    <Text style={styles.textData}>Pianoforte, Chitarra, Python</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Voti: </Text>
                                    <Text style={styles.textData}>4/5</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Recensioni: </Text>
                                    <Text style={styles.textData}>2 recensioni</Text>
                                </View>

                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Annunci di laura" onPress={() => this.props.navigation.navigate('ListaAnnunci')}/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Recensioni ricevute"/>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Modifica profilo"/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Elimina profilo" color='red' onPress={() => this.props.navigation.navigate('EliminaProfiloConferma', {id_utente: id_utente})} />
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
        justifyContent: 'center',
        paddingTop: 20
    },
    buttonview: {
        width: width - width / 1.45,
        paddingLeft: width - width / 1.03,
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

export default ProfiloPetsitter;