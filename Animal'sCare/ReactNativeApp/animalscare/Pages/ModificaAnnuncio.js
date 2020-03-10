import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput, ActivityIndicator } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';
import CheckBox from 'react-native-check-box';
import {Picker} from 'native-base';

const {width, height} = Dimensions.get('window');

class ModificaAnnuncio extends Component {

    constructor(props){
        super(props);
        this.state ={
            id_annuncio: this.props.navigation.state.params.id_annuncio,
            error_message: "",
            chkPasseggiate: false,
            chkPuliziaGabbia: false,
            chkCibo: false,
            chkOreCompagnia: false,
            chkAccompagnaDalVet: false,
            titolo: "",
            sottotitolo: "",
            descrizione: "",
            data_inizio: "",
            data_fine: "",
            pet: "Cane",
            pet_coins: 0,
            logo_annuncio: null
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
            error_message: "",
            chkPasseggiate: responseJson.passeggiate,
            chkPuliziaGabbia: responseJson.pulizia_gabbia,
            chkCibo: responseJson.cibo,
            chkOreCompagnia: responseJson.ore_compagnia,
            chkAccompagnaDalVet: responseJson.accompagna_dal_vet,
            titolo: responseJson.annuncio.titolo,
            sottotitolo: responseJson.annuncio.sottotitolo,
            descrizione: responseJson.annuncio.descrizione,
            data_inizio: responseJson.annuncio.data_inizio,
            data_fine: responseJson.annuncio.data_fine,
            pet_coins: responseJson.annuncio.pet_coins,
            logo_annuncio: null
        }, function(){

        });

        })
        .catch((error) =>{
        this.fetchDettagliAnnuncio();
        });
    }

    modificaAnnuncio = () => {
        if (this.state.titolo != "" && this.state.sottotitolo != "" && this.state.descrizione != "" &&
            this.state.data_inizio != "" && this.state.data_fine != "" && this.state.pet != "" &&
            this.state.pet_coins != 0) {
            fetch('http://2.224.160.133.xip.io/api/annunci/' + this.props.navigation.state.params.id_annuncio + '/dettagli/',
            {
              method: 'PUT',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + global.user_key,
              },
              body: JSON.stringify({
                annuncio: {
                    titolo: this.state.titolo,
                    sottotitolo: this.state.sottotitolo,
                    descrizione: this.state.descrizione,
                    data_inizio: this.state.data_inizio,
                    data_fine: this.state.data_fine,
                    logo_annuncio: this.state.logo_annuncio,
                    pet: this.state.pet,
                    pet_coins: this.state.pet_coins
                },
                passeggiate: this.state.chkPasseggiate,
                pulizia_gabbia: this.state.chkPuliziaGabbia,
                cibo: this.state.chkCibo,
                ore_compagnia: this.state.chkOreCompagnia,
                accompagna_dal_vet: this.state.chkAccompagnaDalVet
              }),
            })
            .then(res => res.json())
            .then((res) => {
                if (res.id != null) {
                    this.props.navigation.goBack(null);
                } else {
                    this.setState({error_message: "Errore: controlla i campi inseriti e riprova."});
                }
            })
            .catch((error) => {
                this.modificaAnnuncio;
            })
        } else {
            this.setState({error_message: "Errore: assicurati di riempire tutti i campi."});
        }
    }

    clearFields = () => {
        this.setState({error_message: "",
        chkPasseggiate: false,
        chkPuliziaGabbia: false,
        chkCibo: false,
        chkOreCompagnia: false,
        chkAccompagnaDalVet: false,
        titolo: "",
        sottotitolo: "",
        descrizione: "",
        data_inizio: "",
        data_fine: "",
        pet_coins: 0,
        logo_annuncio: ""});

        this.txtTitolo.clear();
        this.txtSottotitolo.clear();
        this.txtDescrizione.clear();
        this.txtDataInizio.clear();
        this.txtDataFine.clear();
        this.txtPetCoins.clear();
    }

    render() {
        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Inserisci un nuovo annuncio
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <View style={{flexDirection: 'row'}}>
                                    <View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Titolo:</Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Sottotitolo: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Descrizione: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Data inizio: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Data fine: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pet: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pet coins: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Passeggiate: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pulizia gabbia: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Cibo: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Ore compagnia: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Accompagna dal vet: </Text>
                                        </View>
                                    </View>

                                    <View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} 
                                            value = {this.state.titolo}
                                            ref={input => { this.txtTitolo = input }}
                                            onChangeText={(value) => this.setState({titolo: value})}/>
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} 
                                            value = {this.state.sottotitolo}
                                            ref={input => { this.txtSottotitolo = input }}
                                            onChangeText={(value) => this.setState({sottotitolo: value})}/>
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={245} multiline={true}
                                            value = {this.state.descrizione}
                                            ref={input => { this.txtDescrizione = input }}
                                            onChangeText={(value) => this.setState({descrizione: value})} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={20} multiline={true}
                                            value = {this.state.data_inizio}
                                            ref={input => { this.txtDataInizio = input }}
                                            onChangeText={(value) => this.setState({data_inizio: value})} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={20} multiline={true}
                                            value = {this.state.data_fine}
                                            ref={input => { this.txtDataFine = input }}
                                            onChangeText={(value) => this.setState({data_fine: value})} />
                                        </View>
                                        <View>
                                        <Picker
                                            style={styles.picker} itemStyle={styles.pickerItem}
                                            selectedValue={this.state.pet}
                                            onValueChange={(itemValue) => this.setState({pet: itemValue})}
                                            >
                                            <Picker.Item label="Cane" value="Cane" />
                                            <Picker.Item label="Gatto" value="Gatto" />
                                            <Picker.Item label="Coniglio" value="Coniglio" />
                                            <Picker.Item label="Volatile" value="Volatile" />
                                            <Picker.Item label="Rettile" value="Rettile" />
                                            <Picker.Item label="Altro" value="Altro" />
                                        </Picker>
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={10} multiline={true}
                                            value = {this.state.pet_coins.toString()}
                                            ref={input => { this.txtPetCoins = input }}
                                            onChangeText={(value) => this.setState({pet_coins: value})} />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chkPasseggiate'
                                                onClick={()=>{
                                                    this.setState({
                                                        chkPasseggiate:!this.state.chkPasseggiate
                                                    })
                                                }}
                                                isChecked={this.state.chkPasseggiate}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chkPuliziaGabbia'
                                                onClick={()=>{
                                                    this.setState({
                                                        chkPuliziaGabbia:!this.state.chkPuliziaGabbia
                                                    })
                                                }}
                                                isChecked={this.state.chkPuliziaGabbia}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chkCibo'
                                                onClick={()=>{
                                                    this.setState({
                                                        chkCibo:!this.state.chkCibo
                                                    })
                                                }}
                                                isChecked={this.state.chkCibo}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chkOreCompagnia'
                                                onClick={()=>{
                                                    this.setState({
                                                        chkOreCompagnia:!this.state.chkOreCompagnia
                                                    })
                                                }}
                                                isChecked={this.state.chkOreCompagnia}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chkAccompagnaDalVet'
                                                onClick={()=>{
                                                    this.setState({
                                                        chkAccompagnaDalVet:!this.state.chkAccompagnaDalVet
                                                    })
                                                }}
                                                isChecked={this.state.chkAccompagnaDalVet}
                                            />
                                        </View>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Inserisci annuncio" onPress={() => {
                                            this.modificaAnnuncio();}} />
                                    </View>
                                </View>

                                <View style={{paddingTop: 10}}></View>
                                <Text style={{color: 'red'}}>{this.state.error_message}</Text>
                                <View style={{paddingTop: 10}}></View>

                                <View style={{flexDirection: 'row', marginTop: 20, marginBottom: 5}}>
                                    <Text>I campi contrassegnati con</Text>
                                    <Text style={styles.asteriskStyle}>*</Text>
                                    <Text>sono obbligatori.</Text>

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
        marginVertical: 10
    },
    buttonview: {
        width: 110,
        paddingRight: 5,
        paddingLeft: 5
    },
    inputContainer: {
        minWidth: '96%'
    },
    controlli: {
        paddingTop: 20,
        paddingRight: 5,
        alignItems: 'center'
    },
    data: {
        paddingTop: 20,
        paddingLeft: 10
    },
    entryTitle: {
        marginBottom: 5,
        marginTop: 9,
        flexDirection: 'row'
    },
    textTitle: {
        fontWeight: 'bold'
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
    textContainer: {
        borderWidth: 1,
        height: 28,
        width: width - width / 2,
        marginLeft: 10,
        marginBottom: 3,
        marginTop: 3
    },
    caricaStyle: {
        marginBottom: 3,
        marginTop: 3,
        height: 28,
        width: 100,
        marginLeft: 10,
        borderWidth: 1,
        alignItems: 'center'
    },
    checkBoxStyle: {
        marginLeft: 10,
        marginBottom: 6,
        marginTop: 3
    },
    asteriskStyle: {
        marginLeft: 3,
        marginRight: 3,
        color: 'red'
    },
    picker: {
        marginLeft: 10,
        width: width - width / 2,
        height: 28,
        backgroundColor: '#e7e7e7',
        marginBottom: 3,
        marginTop: 3
    },
    pickerItem: {
        color: 'white'
    }
});

export default ModificaAnnuncio;