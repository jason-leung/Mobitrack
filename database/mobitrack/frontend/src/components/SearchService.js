import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default class SearchService{
	constructor(){}

	getSessionByID(sessionID) {
		const url = '${API_URL}/database/wearingsession/${sessionID}';
		return axios.get(url).then(response => response.data);
	}
}


