import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions, ActivityIndicator } from 'react-native';
import { IconButton } from 'react-native-paper';
import { Picker } from 'native-base';
import PickerProvince from '../components/PickerProvince';
import PickerRegioni from '../components/PickerRegioni';

const {width, height} = Dimensions.get('window');

class ModificaProfilo extends Component {

    constructor(props){
        super(props);
        this.state ={
            error_message: "",
            username: "",
            password: "",
            conferma_password: "",
            nome: "",
            cognome: "",
            email: "",
            indirizzo: "",
            citta: "",
            telefono: "",

            nome_pet: "",
            razza: "",
            eta: 0,
            caratteristiche: "",
            pet: "Cane",

            descrizione: "",
            hobby: ""
        }
    }

    componentDidMount() {
        this.fetchProfilo();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.fetchProfilo();
          }
        );
    }

    componentWillUnmount() {
    this.willFocusSubscription.remove();
    }

    fetchProfilo() {
        return fetch('http://2.224.160.133.xip.io/api/utenti/profilo/' + global.user_id + '/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {
        
        this.setState({
            isLoading: false,
            username: responseJson.user.username,
            nome: responseJson.user.first_name,
            cognome: responseJson.user.last_name,
            email: responseJson.user.email,
            indirizzo: responseJson.indirizzo,
            citta: responseJson.citta,
            telefono: responseJson.telefono
        }, function(){

        });

        global.provincia = responseJson.provincia;
        global.regione = responseJson.regione;

        if (global.is_petsitter == false) {
            this.setState({
                nome_pet: responseJson.nome_pet,
                pet: responseJson.pet,
                razza: responseJson.razza,
                eta: responseJson.eta,
                caratteristiche: responseJson.caratteristiche
            }, function(){
    
            });
        } else {
            this.setState({
                descrizione: responseJson.descrizione,
                hobby: responseJson.hobby
            }, function(){
    
            });
        }

        })
        .catch((error) =>{
        this.fetchProfilo();
        });
    }

    modificaProfiloNormale = () => {
        if (this.state.username != "" && this.state.password != "" && this.state.conferma_password != "" &&
            this.state.nome != "" && this.state.cognome != "" && this.state.pet != "" &&
            this.state.email != "" && this.state.indirizzo != "" && this.state.citta != "" &&
            this.state.telefono != "" && this.state.nome_pet != "" && this.state.razza != "" &&
            this.state.eta != "" && this.state.caratteristiche != "") {
            if (this.state.password == this.state.conferma_password) {
                fetch('http://2.224.160.133.xip.io/api/utenti/profilo/',
                {
                method: 'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + global.user_key,
                },
                body: JSON.stringify({
                    user: {
                        username: this.state.username,
                        password: this.state.password,
                        first_name: this.state.nome,
                        last_name: this.state.cognome,
                        email: this.state.email
                    },
                    indirizzo: this.state.indirizzo,
                    citta: this.state.citta,
                    provincia: global.provincia,
                    regione: global.regione,
                    telefono: this.state.telefono,
                    nome_pet: this.state.nome_pet,
                    pet: this.state.pet,
                    razza: this.state.razza,
                    eta: this.state.eta,
                    caratteristiche: this.state.caratteristiche
                }),
                })
                .then(res => res.json())
                .then((res) => {
                    if (res.user.id != null) {
                        global.username = this.state.username;

                        this.clearFields();
                        this.props.navigation.navigate("ListaAnnunci");
                    } else {
                        this.setState({error_message: "Errore: " + JSON.stringify(res)});
                    }
                })
                .catch((error) => {
                    this.setState({error_message: "Errore: " + error});
                    this.modificaProfilo;
                })
            }
        }       
    }

    modificaProfiloPetsitter = () => {
        if (this.state.username != "" && this.state.password != "" && this.state.conferma_password != "" &&
            this.state.nome != "" && this.state.cognome != "" &&
            this.state.email != "" && this.state.indirizzo != "" && this.state.citta != "" &&
            this.state.telefono != "" &&
            this.state.descrizione != "" && this.state.hobby != "") {
            if (this.state.password == this.state.conferma_password) {

                fetch('http://2.224.160.133.xip.io/api/utenti/profilo/',
                {
                method: 'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + global.user_key,
                },
                body: JSON.stringify({
                    user: {
                        username: this.state.username,
                        password: this.state.password,
                        first_name: this.state.nome,
                        last_name: this.state.cognome,
                        email: this.state.email
                    },
                    indirizzo: this.state.indirizzo,
                    citta: this.state.citta,
                    provincia: global.provincia,
                    regione: global.regione,
                    telefono: this.state.telefono,
                    descrizione: this.state.descrizione,
                    hobby: this.state.hobby
                }),
                })
                .then(res => res.json())
                .then((res) => {
                    if (res.user.id != null) {
                        global.username = this.state.username;
                        
                        this.clearFields();
                        this.props.navigation.navigate("ListaAnnunci");
                    } else {
                        this.setState({error_message: "Errore: " + JSON.stringify(res)});
                    }
                })
                .catch((error) => {
                    this.setState({error_message: "Errore: " + error});
                    this.modificaProfilo;
                })
            }
        }       
    }

    clearFields = () => {
        this.setState({error_message: "",
            username: "",
            password: "",
            conferma_password: "",
            nome: "",
            cognome: "",
            email: "",
            indirizzo: "",
            citta: "",
            telefono: "",

            nome_pet: "",
            razza: "",
            eta: "",
            caratteristiche: "",
            pet: "Cane",

            descrizione: "",
            hobby: ""
        });

        this.txtUsername.clear();
        this.txtPassword.clear();
        this.txtConfermaPassword.clear();
        this.txtNome.clear();
        this.txtCognome.clear();
        this.txtEmail.clear();
        this.txtIndirizzo.clear();
        this.txtCitta.clear();
        this.txtTelefono.clear();

        if (global.is_petsitter == false) {
            this.txtNomePet.clear();
            this.txtRazza.clear();
            this.txtEta.clear();
            this.txtCaratteristiche.clear();
        } else {
            this.txtDescrizione.clear();
            this.txtHobby.clear();
        }
    }
    
    render() {
        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        if (globalThis.is_petsitter == false) {
            return (
                
                <View style={styles.screen}>
                    <CustomHeader parent={this.props} />
                    
                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Modifica profilo
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
                                                <Text style={styles.textTitle}>Username:</Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Password: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Conferma password: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Nome: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Cognome: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Email: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Indirizzo: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Città: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Provincia: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Regione: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Telefono: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Nome pet: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Pet: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Razza: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Età: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Caratteristiche: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                        </View>
    
                                        <View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.username}
                                                ref={input => { this.txtUsername = input }}
                                                onChangeText={(value) => this.setState({username: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95} secureTextEntry={true}
                                                ref={input => { this.txtPassword = input }}
                                                onChangeText={(value) => this.setState({password: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95} secureTextEntry={true}
                                                ref={input => { this.txtConfermaPassword = input }}
                                                onChangeText={(value) => this.setState({conferma_password: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.nome}
                                                ref={input => { this.txtNome = input }}
                                                onChangeText={(value) => this.setState({nome: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.cognome}
                                                ref={input => { this.txtCognome = input }}
                                                onChangeText={(value) => this.setState({cognome: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.email}
                                                ref={input => { this.txtEmail = input }}
                                                onChangeText={(value) => this.setState({email: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.indirizzo}
                                                ref={input => { this.txtIndirizzo = input }}
                                                onChangeText={(value) => this.setState({indirizzo: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.citta}
                                                ref={input => { this.txtCitta = input }}
                                                onChangeText={(value) => this.setState({citta: value})}/>
                                            </View>
                                            <PickerProvince />
                                            <PickerRegioni />
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.telefono}
                                                ref={input => { this.txtTelefono = input }}
                                                onChangeText={(value) => this.setState({telefono: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.nome_pet}
                                                ref={input => { this.txtNomePet = input }}
                                                onChangeText={(value) => this.setState({nome_pet: value})}/>
                                            </View>
                                            <Picker
                                                style={styles.picker} itemStyle={styles.pickerItem}
                                                selectedValue={this.state.pet}
                                                onValueChange={(itemValue) => this.setState({pet: itemValue})}
                                                >
                                                <Picker.Item label="Cane" value="cane" />
                                                <Picker.Item label="Gatto" value="gatto" />
                                                <Picker.Item label="Coniglio" value="coniglio" />
                                                <Picker.Item label="Volatile" value="volatile" />
                                                <Picker.Item label="Rettile" value="rettile" />
                                                <Picker.Item label="Altro" value="altro" />
                                            </Picker>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.razza}
                                                ref={input => { this.txtRazza = input }}
                                                onChangeText={(value) => this.setState({razza: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.eta.toString()}
                                                ref={input => { this.txtEta = input }}
                                                onChangeText={(value) => this.setState({eta: value})}/>
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.caratteristiche}
                                                ref={input => { this.txtCaratteristiche = input }}
                                                onChangeText={(value) => this.setState({caratteristiche: value})}/>
                                            </View>
                                        </View>
                                    </View>
                                    <View style={styles.controlli}>
                                        <View style={styles.buttonview}>
                                            <Button title="Applica modifiche" onPress={() => {
                                                this.modificaProfiloNormale();}} />
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
        } else {
            return (
                
                <View style={styles.screen}>
                    <CustomHeader parent={this.props} />
                    
                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Modifica profilo
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
                                                <Text style={styles.textTitle}>Username:</Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Password: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Conferma password: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Nome: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Cognome: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Email: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Indirizzo: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Città: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Provincia: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Regione: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Telefono: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Descrizione: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                            <View style={styles.entryTitle}>
                                                <Text style={styles.textTitle}>Hobby: </Text>
                                                <Text style={styles.asteriskStyle}>*</Text>
                                            </View>
                                        </View>
    
                                        <View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.username}
                                                ref={input => { this.txtUsername = input }}
                                                onChangeText={(value) => this.setState({username: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95} secureTextEntry={true}
                                                ref={input => { this.txtPassword = input }}
                                                onChangeText={(value) => this.setState({password: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95} secureTextEntry={true}
                                                ref={input => { this.txtConfermaPassword = input }}
                                                onChangeText={(value) => this.setState({conferma_password: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.nome}
                                                ref={input => { this.txtNome = input }}
                                                onChangeText={(value) => this.setState({nome: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.cognome}
                                                ref={input => { this.txtCognome = input }}
                                                onChangeText={(value) => this.setState({cognome: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.email}
                                                ref={input => { this.txtEmail = input }}
                                                onChangeText={(value) => this.setState({email: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.indirizzo}
                                                ref={input => { this.txtIndirizzo = input }}
                                                onChangeText={(value) => this.setState({indirizzo: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.citta}
                                                ref={input => { this.txtCitta = input }}
                                                onChangeText={(value) => this.setState({citta: value})} />
                                            </View>
                                            <PickerProvince />
                                            <PickerRegioni />
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.telefono}
                                                ref={input => { this.txtTelefono = input }}
                                                onChangeText={(value) => this.setState({telefono: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.descrizione}
                                                ref={input => { this.txtDescrizione = input }}
                                                onChangeText={(value) => this.setState({descrizione: value})} />
                                            </View>
                                            <View style={styles.textContainer}>
                                                <TextInput editable maxLength={95}
                                                value={this.state.hobby}
                                                ref={input => { this.txtHobby = input }}
                                                onChangeText={(value) => this.setState({hobby: value})} />
                                            </View>
                                        </View>
                                    </View>
                                    <View style={styles.controlli}>
                                        <View style={styles.buttonview}>
                                            <Button title="Applica modifiche" onPress={() => {
                                                this.modificaProfiloPetsitter();}} />
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

export default ModificaProfilo;