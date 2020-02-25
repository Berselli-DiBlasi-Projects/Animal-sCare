import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions, ActivityIndicator, FlatList, YellowBox } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import annuncio_default from '../assets/annuncio_default.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class ListaAnnunci extends Component {

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true,
            categorie: "tutto",
            animali: "tutto",
            ordina: "non_ordinare",
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
    
    componentDidMount(){
    return fetch('http://2.224.160.133.xip.io/api/annunci/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {

        this.setState({
            isLoading: false,
            dataSource: responseJson,
        }, function(){

        });

        })
        .catch((error) =>{
        console.error(error);
        });
    }

    render() {

        if(this.state.isLoading){
            return(
                <View style={{flex: 1, padding: 20}}>
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
                        <View style={styles.leftcontainer}></View>
                        <Text style={styles.title}>
                            Annunci
                        </Text>
                        <View style={styles.rightcontainer}>
                            <IconButton icon="filter" style={{paddingRight: 10}} onPress={this.ShowHidePickers} />
                        </View>
                    </View>
                    
                    {this.state.show_pickers ? (
                        <View style={styles.pickers}>
                            <Picker
                                style={styles.picker} itemStyle={styles.pickerItem}
                                selectedValue={this.state.categorie}
                                onValueChange={(itemValue) => this.setState({categorie: itemValue})}
                                >
                                <Picker.Item label="Tutte le categorie di annunci" value="tutto" />
                                <Picker.Item label="Cerco un petsitter" value="petsitter" />
                                <Picker.Item label="Cerco un pet" value="pet" />
                            </Picker>

                            <View style={{paddingBottom: 5}}></View>
                        
                            <Picker
                                style={styles.picker} itemStyle={styles.pickerItem}
                                selectedValue={this.state.animali}
                                onValueChange={(itemValue) => this.setState({animali: itemValue})}
                                >
                                <Picker.Item label="Tutti gli animali" value="tutto" />
                                <Picker.Item label="Cani" value="cani" />
                                <Picker.Item label="Gatti" value="gatti" />
                                <Picker.Item label="Conigli" value="conigli" />
                                <Picker.Item label="Volatili" value="volatili" />
                                <Picker.Item label="Rettili" value="rettili" />
                                <Picker.Item label="Altro" value="altro" />
                            </Picker>

                            <View style={{paddingBottom: 5}}></View>

                            <Picker
                                style={styles.picker} itemStyle={styles.pickerItem}
                                selectedValue={this.state.ordina}
                                onValueChange={(itemValue) => this.setState({ordina: itemValue})}
                                >
                                <Picker.Item label="Non ordinare gli annunci" value="non_ordinare" />
                                <Picker.Item label="Distanza geografica crescente" value="crescente" />
                                <Picker.Item label="Distanza geografica decrescente" value="decrescente" />
                            </Picker>

                            <View style={{paddingBottom: 2}}></View>
                        </View>
                    ) : null}
                </View>
                <View style={styles.flatlistview}>
                    <FlatList
                        style={{flex: 1}}
                        data={this.state.dataSource}
                        renderItem={({item}) => 
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: item.id})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={ item.logo_annuncio ? { uri: item.logo_annuncio } : annuncio_default }
                                    style={styles.annuncioLogo}
                                />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.annuncioTitle} numberOfLines={1}>{item.titolo}</Text>
                                    
                                    <Text style={styles.annuncioSubtitle} numberOfLines={2}>{item.sottotitolo}</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Data: </Text>
                                        <Text>{item.data_inizio} {item.data_fine}</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Pubblicato da: </Text>
                                        <Text>{item.user}</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
                        }
                        keyExtractor={({id}, index) => id.toString()}
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
    annuncioLogo: {
        width: 80,
        height: 80
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
    annuncioTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    annuncioSubtitle: {
        width: width - width / 2.6
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
        height: 132,
        width: '90%',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    flatlistview: {
        flex: 1,
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center'
    }
});

export default ListaAnnunci;