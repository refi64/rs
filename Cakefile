{print} = require 'sys'
{spawn} = require 'child_process'

run = (cmd) ->
  print "#{cmd}\n"
  [prog, argl...] = cmd.split ' '
  pipe = spawn prog, argl
  pipe.stderr.on 'data', (data) -> process.stderr.write data.toString()
  pipe.stdout.on 'data', (data) -> print data.toString()

coffee = (args='') -> run "coffee #{args} -o js -c src/load.coffee"

task 'build', 'build load.js', -> coffee()
task 'watch', 'watch load.coffee and rebuild', -> coffee '-w'
