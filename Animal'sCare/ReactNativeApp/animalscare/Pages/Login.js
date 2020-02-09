import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class Login extends Component {

    render() {
        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Log in
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
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Password: </Text>
                                        </View>
                                    </View>

                                    <View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Accedi" />
                                    </View>
                                </View>

                                <View style={{paddingTop: 25}}></View>
                                <View style={{borderBottomColor: 'black', borderBottomWidth: 1, width: width - (width * 10 / 100)}}></View>
                                <View style={{paddingTop: 25}}></View>

                                <View style={{flexDirection: 'row'}}>
                                    <View>
                                        <View style={styles.bottomTitle}>
                                            <Text style={styles.textTitle}>Non hai un account?</Text>
                                        </View>
                                        <View style={styles.bottomTitle}>
                                            <Text style={styles.textTitle}>Oppure: </Text>
                                        </View>
                                    </View>

                                    <View>
                                        <View style={styles.bottomButton}>
                                            <Button title="Registrati" onPress={() => this.props.navigation.navigate('Registrazione')}/>
                                        </View>
                                        <View style={styles.bottomButton}>
                                            <Button title="Login con Google" />
                                        </View>
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
        alignItems: 'center'
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
    bottomButton: {
        width: 110,
        paddingRight: 5,
        paddingLeft: 10,
        paddingBottom: 10
    },
    bottomTitle: {
        marginBottom: 25,
        marginTop: 9,
        alignItems: 'flex-end'
    }
});

export default Login;