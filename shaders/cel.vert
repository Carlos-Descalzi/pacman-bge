//Interpolates the vertex normal across the texture fragment
varying vec3 normal;
//Interpolate the texel position in eye space.
varying vec3 ec_pos;
varying vec3 l_target;

varying vec2 texture_coordinate;

varying vec3 camera_pos;
varying vec3 camera_dir;

void main()
{
	normal = gl_NormalMatrix * gl_Normal;
	ec_pos = vec3(gl_ModelViewMatrix * gl_Vertex);
	l_target = vec3(gl_ModelViewMatrix * vec4(0.0,0.0,0.0,0.0));

	camera_pos = vec3(gl_ModelViewMatrix[3]);
	camera_dir = vec3(gl_ModelViewMatrix[2]);
	
	//Perform fixed transformation for the vertex
	gl_Position = ftransform();	
	texture_coordinate = vec2(gl_MultiTexCoord0);	
}
