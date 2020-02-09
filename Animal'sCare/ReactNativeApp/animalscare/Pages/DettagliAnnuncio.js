import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import logo from '../assets/fac-simile.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import AutoHeightImage from 'react-native-auto-height-image';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

let id_annuncio;

class DettagliAnnuncio extends Component {

    render() {
        id_annuncio = this.props.navigation.state.params.id_annuncio;
        
        return (
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Annuncio n. {id_annuncio}
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>
                
                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        <AutoHeightImage width={width - width / 30} source={logo} />

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Sottotitolo: </Text>
                                    <Text style={styles.textData}>Bobi cerca un petsitter e bla bla bla bla bla bla bla bla bla bla</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Descrizione: </Text>
                                    <Text style={styles.textData}>Lorem Ipsum è un testo segnaposto utilizzato nel settore della tipografia e della stampa. Lorem Ipsum è considerato il testo segnaposto standard sin dal sedicesimo secolo, quando un anonimo tipografo prese una cassetta di caratteri e li assemblò per preparare un testo campione</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Pubblicato da: </Text>
                                    <Text style={styles.textData}>werther</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Pet: </Text>
                                    <Text style={styles.textData}>Cane</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Data inizio: </Text>
                                    <Text style={styles.textData}>11/11/2020 15:00</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Data fine: </Text>
                                    <Text style={styles.textData}>12/11/2020 15:00</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Posizione: </Text>
                                    <Text style={styles.textData}>INSERIRE MAPPA</Text>
                                </View>
                                <View style={styles.entry}>
                                    <Text style={styles.textTitle}>Servizi richiesti: </Text>
                                    <Text style={styles.textData}>Passeggiate, ore di compagnia</Text>
                                </View>

                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Accetta annuncio" onPress={() => this.props.navigation.navigate('AccettaAnnuncioConferma', {id_annuncio: id_annuncio})}/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Modifica annuncio" onPress={() => this.props.navigation.navigate('ModificaAnnuncio')}/>
                                    </View>
                                    <View style={styles.buttonview}>
                                        <Button title="Elimina annuncio" color='red' onPress={() => this.props.navigation.navigate('EliminaAnnuncioConferma', {id_annuncio: id_annuncio})} />
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