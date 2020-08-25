import { Server, Model, Factory, Response, belongsTo } from "miragejs"
import faker from "faker"

const config = {
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL,
  namespace: process.env.REACT_APP_API_NAMESPACE,
  lowLatencyTime: 100,  
  highLatencyTime: 1000,
  tokenValue: "TEST_TOKEN_VALUE",
  // testImageUrl: "https://pyvinci-storage.s3.amazonaws.com/users/97e1d77e-3d79-4bab-b21e-f0f1e775fa19/projects/ae027201-77dd-49e9-a5c9-e20333df0f45/3a0f255e-aff1-47d7-8e46-c9c03a99a823_1366003382850.jpg"
}

export function makeServer({ environment = "test" } = {}) {
  let server = new Server({
    // serializers: {
    //   application: RestSerializer,
    // },
    models: {
      project: Model,
      user: Model,
      image: Model.extend({
        project: belongsTo(),
      }),
      job: Model
    },

    factories: {
      project: Factory.extend({
        name() {
          return `Project ${faker.name.firstName()}`
        },
        keywords() {
          return null
        },
        labels() {
          return null
        },
        status() {
          return ""
        },
      }),
      user: Factory.extend({
        // id() {
        //   return faker.random.uuid()
        // },
        username() {
          return faker.internet.userName()
        },
        createAt() {
          return faker.date.past()
        },
        updatedAt() {
          return faker.date.past()
        },
        // Not available in Register response
        token() {
          return config.tokenValue
        },
        // Not available in Register response
        expireAt() {
          return faker.date.future()
        }
      }),
      image: Factory.extend({
        // id() {
        //   return faker.random.uuid()
        // },
        url() {
          return faker.internet.url()
          // return config.testImageUrl
        },
        createdAt() {
          return faker.date.past()
        },
        updatedAt() {
          return faker.date.past()
        },
      }),
      job: Factory.extend({
        jobId(){
          return faker.random.jobId()
        },
        status(){
          return "PENDING_LABELS"
        }
      })
    },

    seeds(server) {  
      server.createList("user", 1)
      server.createList("project", 2).forEach((project) => {
        server.createList("image", 2, {project})
      })
    },

    routes() {
      this.urlPrefix = config.apiBaseUrl;
      this.namespace = config.namespace;

      /**
       * Auth
       */
      this.post("auth/register", ({users}) => {
        return users.find(1).attrs
      },
      {
        // timing: config.lowLatencyTime
      })
      this.post("auth/login", ({users}) => {
        return users.find(1).attrs
      },
      {
        // timing: config.lowLatencyTime
      })

      /**
       * Projects
       */
      this.get("/users/:userId/projects", (schema, request) => {
        if(request.requestHeaders["authorization"] !== `Bearer ${config.tokenValue}`) {
          return new Response(401, {}, { error: 'No Authorization header provided.'});
        }
        return new Response(
          200, 
          {}, 
          {
            projects: schema.db.projects
          }
        )
      })
      this.get("/users/:userId/projects/:projectId", (schema, request) => {
        let projectId = request.params.projectId
        return new Response(
          200,
          {},
          {
            project: schema.db.projects.find(projectId)
          }
        )
      })
      this.post("/users/:userId/projects", (schema, request) => {
        const { name } = JSON.parse(request.requestBody)
        return new Response(
          200,
          {},
          {
            project: schema.db.projects.insert({name: name})
          }
        )
      })

      /**
       * Images
       */
      this.get("users/:userId/projects/:projectId/images", (schema, request) => {
        let projectId = request.params.projectId
        return new Response(
          200,
          {},
          {
            images: schema.db.images.where({projectId: projectId})
          }
        )
      })
      this.post("users/:userId/projects/:projectId/images", (schema, request) => {
        let projectId = request.params.projectId

        // Check multipart form data included?
        if(!request.sendArguments[0].get("images")){
          return new Response(500, {}, { error: 'No Formdata.images included in request'});
        }

        // Add image
        schema.db.images.insert({
          createdAt: faker.date.past(),
          updatedAt: faker.date.past(),
          url: faker.internet.url(),
          // url: config.testImageUrl,
          projectId: projectId,
        })

        return new Response(
          200,
          {},
          {
            images: schema.db.images.where({projectId: projectId})
          }
        )
      })
      this.delete("users/:userId/projects/:projectId/images/:imageId", (schema, request) => {
        let { imageId } = request.params

        schema.db.images.remove(imageId)

        return new Response(
          200,
          {},
          {}
        )
      })

      /**
       * Jobs
       */
      this.post("users/:userId/projects/:projectId/job", (schema, request) => {

        const { projectId } = request.params
        
        const job = schema.db.jobs.insert()

        // Set project status to PENDING_LABELS
        var project = schema.projects.find(projectId)
        project.update({status: "PENDING_LABELS"})

        // Update project status to completed
        const updateProjectStatus = () => {
          console.log("Updating project status to COMPLETED")
          var project = schema.projects.find(projectId)
          project.update({status: "COMPLETED"})
        }
        // After 5 seconds
        setTimeout(updateProjectStatus, 5000);

        return new Response(
          201,
          {},
          job
        )
      })
    },
  })

  return server
}