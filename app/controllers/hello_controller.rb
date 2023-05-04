class HelloController < ApplicationController
    def index
        sample = {
            message: "hello world!"
        }
        render json: sample
    end
end
