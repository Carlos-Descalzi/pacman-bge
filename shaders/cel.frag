varying vec3 normal;
varying vec3 ec_pos;

varying vec2 texture_coordinate;
uniform sampler2D my_color_texture;

varying vec3 camera_pos;
varying vec3 camera_dir;

float discrete(float val, float slices){
	return float(int(val*slices))/slices;
}


float get_diffuse(int lightIndex){
	vec3 light = vec3( gl_LightSource[lightIndex].position );
	float diff = max( dot(normalize(light), normalize(normal)), 0.0);
	return diff;
}

void main()
{
	vec4 color = texture2D(my_color_texture, texture_coordinate);

	float diff = 3.0 * (get_diffuse(0) * 0.3 + get_diffuse(1) * 0.7);
		
	diff = max(0.1,discrete(diff,2));

	gl_FragColor = color * diff;
}

